from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import IsAuthenticated

from .models       import RiderProfile
from .serializers  import RiderProfileSerializer, RiderAvailabilitySerializer, RiderLocationSerializer


class RiderProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get the logged-in rider's profile."""
        try:
            profile    = RiderProfile.objects.get(user=request.user)
            serializer = RiderProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RiderProfile.DoesNotExist:
            return Response(
                {'detail': 'Rider profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        """Create a rider profile (only for users with role=rider)."""
        if request.user.role != 'rider':
            return Response(
                {'detail': 'Only riders can create a rider profile.'},
                status=status.HTTP_403_FORBIDDEN
            )
        if RiderProfile.objects.filter(user=request.user).exists():
            return Response(
                {'detail': 'Rider profile already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RiderProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Update the logged-in rider's profile."""
        try:
            profile    = RiderProfile.objects.get(user=request.user)
            serializer = RiderProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RiderProfile.DoesNotExist:
            return Response(
                {'detail': 'Rider profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class RiderAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        """Toggle rider availability on/off."""
        try:
            profile    = RiderProfile.objects.get(user=request.user)
            serializer = RiderAvailabilitySerializer(data=request.data)
            if serializer.is_valid():
                profile.is_available = serializer.validated_data['is_available']
                profile.save()
                return Response(
                    {'detail': f"Availability set to {profile.is_available}."},
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RiderProfile.DoesNotExist:
            return Response(
                {'detail': 'Rider profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class RiderLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        """Update rider's current GPS location."""
        try:
            profile    = RiderProfile.objects.get(user=request.user)
            serializer = RiderLocationSerializer(data=request.data)
            if serializer.is_valid():
                profile.current_lat = serializer.validated_data['current_lat']
                profile.current_lng = serializer.validated_data['current_lng']
                profile.save()
                return Response(
                    {'detail': 'Location updated.', 'lat': str(profile.current_lat), 'lng': str(profile.current_lng)},
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RiderProfile.DoesNotExist:
            return Response(
                {'detail': 'Rider profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class NearbyRidersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all available and approved riders (customers use this)."""
        riders     = RiderProfile.objects.filter(is_available=True, is_approved=True)
        serializer = RiderProfileSerializer(riders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)