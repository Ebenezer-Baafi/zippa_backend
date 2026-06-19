from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import IsAuthenticated

from .models        import Negotiation
from .serializers   import NegotiationSerializer, NegotiationCreateSerializer, NegotiationResponseSerializer
from jobs.models    import DeliveryJob


class NegotiationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        """Customer or rider initiates a fare negotiation on a job."""
        try:
            job = DeliveryJob.objects.get(id=job_id)
        except DeliveryJob.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # job must be pending to negotiate
        if job.status != 'pending':
            return Response(
                {'detail': 'Can only negotiate on pending jobs.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # determine receiver
        if request.user == job.customer:
            receiver = job.rider.user if job.rider else None
        elif request.user.role == 'rider':
            receiver = job.customer
        else:
            return Response(
                {'detail': 'You are not part of this job.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not receiver:
            return Response(
                {'detail': 'No rider assigned to negotiate with yet.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # check no active pending negotiation exists
        if Negotiation.objects.filter(job=job, status='pending').exists():
            return Response(
                {'detail': 'A negotiation is already pending for this job.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NegotiationCreateSerializer(data=request.data)
        if serializer.is_valid():
            negotiation = Negotiation.objects.create(
                job      = job,
                sender   = request.user,
                receiver = receiver,
                amount   = serializer.validated_data['amount'],
                note     = serializer.validated_data.get('note', ''),
            )
            return Response(
                NegotiationSerializer(negotiation).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NegotiationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        """Get all negotiations for a specific job."""
        try:
            job = DeliveryJob.objects.get(id=job_id)
        except DeliveryJob.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        negotiations = Negotiation.objects.filter(job=job).order_by('created_at')
        serializer   = NegotiationSerializer(negotiations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NegotiationResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, negotiation_id):
        """Receiver responds to a negotiation — accept, reject, or counter."""
        try:
            negotiation = Negotiation.objects.get(id=negotiation_id)
        except Negotiation.DoesNotExist:
            return Response(
                {'detail': 'Negotiation not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # only the receiver can respond
        if request.user != negotiation.receiver:
            return Response(
                {'detail': 'Only the receiver can respond to this negotiation.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if negotiation.status != 'pending':
            return Response(
                {'detail': 'This negotiation has already been responded to.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NegotiationResponseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_status = serializer.validated_data['status']
        negotiation.status = new_status
        negotiation.save()

        # if accepted, update the job's estimated fare
        if new_status == 'accepted':
            job = negotiation.job
            job.estimated_fare = negotiation.amount
            job.save()

        # if countered, create a new negotiation in reverse
        if new_status == 'countered':
            counter_amount = serializer.validated_data.get('amount')
            if not counter_amount:
                return Response(
                    {'detail': 'Amount is required when countering.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Negotiation.objects.create(
                job      = negotiation.job,
                sender   = request.user,
                receiver = negotiation.sender,
                amount   = counter_amount,
                note     = serializer.validated_data.get('note', ''),
            )

        return Response(
            NegotiationSerializer(negotiation).data,
            status=status.HTTP_200_OK
        )