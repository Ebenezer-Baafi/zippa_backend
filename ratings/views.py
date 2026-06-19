from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import IsAuthenticated
from django.db.models           import Avg

from .models        import Rating
from .serializers   import RatingSerializer, RatingCreateSerializer
from jobs.models    import DeliveryJob
from riders.models  import RiderProfile


class CreateRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        """Customer rates a rider after delivery is completed."""
        try:
            job = DeliveryJob.objects.get(id=job_id)
        except DeliveryJob.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # only the customer of this job can rate
        if request.user != job.customer:
            return Response(
                {'detail': 'Only the customer of this job can leave a rating.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # job must be delivered
        if job.status != 'delivered':
            return Response(
                {'detail': 'You can only rate a completed delivery.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # check if already rated
        if Rating.objects.filter(job=job).exists():
            return Response(
                {'detail': 'You have already rated this delivery.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not job.rider:
            return Response(
                {'detail': 'No rider assigned to this job.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RatingCreateSerializer(data=request.data)
        if serializer.is_valid():
            rating = Rating.objects.create(
                job      = job,
                customer = request.user,
                rider    = job.rider.user,
                score    = serializer.validated_data['score'],
                comment  = serializer.validated_data.get('comment', ''),
            )

            # update rider's average rating
            rider_profile = job.rider
            avg = Rating.objects.filter(rider=job.rider.user).aggregate(Avg('score'))['score__avg']
            rider_profile.rating = round(avg, 2)
            rider_profile.save()

            return Response(
                RatingSerializer(rating).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RiderRatingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, rider_id):
        """Get all ratings for a specific rider."""
        ratings    = Rating.objects.filter(rider__id=rider_id).order_by('-created_at')
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyRatingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Rider sees all their own ratings."""
        if request.user.role != 'rider':
            return Response(
                {'detail': 'Only riders can view their ratings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        ratings    = Rating.objects.filter(rider=request.user).order_by('-created_at')
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)