from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import IsAuthenticated
from django.utils               import timezone

from .models        import DeliveryJob
from .serializers   import DeliveryJobSerializer, JobStatusUpdateSerializer
from riders.models  import RiderProfile

from notifications.utils import send_notification


class CreateJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Customer creates a new delivery job."""
        if request.user.role != 'customer':
            return Response(
                {'detail': 'Only customers can create jobs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = DeliveryJobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Customers see their own jobs.
        Riders see all pending jobs available to accept.
        """
        if request.user.role == 'customer':
            jobs = DeliveryJob.objects.filter(customer=request.user).order_by('-created_at')
        elif request.user.role == 'rider':
            jobs = DeliveryJob.objects.filter(status='pending').order_by('-created_at')
        else:
            return Response(
                {'detail': 'Unauthorized.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = DeliveryJobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        """Get details of a specific job."""
        try:
            job = DeliveryJob.objects.get(id=job_id)
            serializer = DeliveryJobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DeliveryJob.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class JobStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, job_id):
        """Rider updates job status."""
        try:
            job = DeliveryJob.objects.get(id=job_id)
        except DeliveryJob.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # only riders can update status
        if request.user.role != 'rider':
            return Response(
                {'detail': 'Only riders can update job status.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            rider_profile = RiderProfile.objects.get(user=request.user)
        except RiderProfile.DoesNotExist:
            return Response(
                {'detail': 'Rider profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobStatusUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_status = serializer.validated_data['status']

        # status transition rules
        valid_transitions = {
            'pending'   : ['accepted', 'cancelled'],
            'accepted'  : ['picked_up', 'cancelled'],
            'picked_up' : ['delivered'],
        }

        if job.status not in valid_transitions or new_status not in valid_transitions.get(job.status, []):
            return Response(
                {'detail': f"Cannot move job from '{job.status}' to '{new_status}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # assign rider on accept
        if new_status == 'accepted':
            job.rider       = rider_profile
            job.accepted_at = timezone.now()
            send_notification(
                user    = job.customer,
                type    = 'job_accepted',
                title   = 'Rider Accepted Your Job!',
                message = f'{rider_profile.user.full_name} has accepted your delivery job.'
            )
        elif new_status == 'picked_up':
            job.picked_up_at = timezone.now()
            send_notification(
                user    = job.customer,
                type    = 'job_picked_up',
                title   = 'Your Package Has Been Picked Up!',
                message = f'{rider_profile.user.full_name} has picked up your package and is on the way.'
            )
        elif new_status == 'delivered':
            job.delivered_at = timezone.now()
            job.final_fare   = job.estimated_fare
            send_notification(
                user    = job.customer,
                type    = 'job_delivered',
                title   = 'Package Delivered!',
                message = f'Your package has been delivered successfully by {rider_profile.user.full_name}.'
            )

        job.status = new_status
        job.save()

        return Response(DeliveryJobSerializer(job).data, status=status.HTTP_200_OK)


class CustomerJobCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, job_id):
        """Customer cancels their own pending job."""
        try:
            job = DeliveryJob.objects.get(id=job_id, customer=request.user)
        except DeliveryJob.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if job.status != 'pending':
            return Response(
                {'detail': 'You can only cancel a pending job.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        job.status = 'cancelled'
        job.save()
        return Response(
            {'detail': 'Job cancelled successfully.'},
            status=status.HTTP_200_OK
        )