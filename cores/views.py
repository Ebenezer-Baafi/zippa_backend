import requests
from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import IsAuthenticated
from decouple import config

GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')

BASE_FARE        = 5.00   # base fare in cedis
FARE_PER_KM      = 2.50   # fare per kilometer
MINIMUM_FARE     = 10.00  # minimum fare


def calculate_fare(distance_km):
    fare = BASE_FARE + (distance_km * FARE_PER_KM)
    return round(max(fare, MINIMUM_FARE), 2)


class FareEstimationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Estimate fare based on pickup and dropoff coordinates."""
        pickup_lat   = request.data.get('pickup_lat')
        pickup_lng   = request.data.get('pickup_lng')
        dropoff_lat  = request.data.get('dropoff_lat')
        dropoff_lng  = request.data.get('dropoff_lng')

        if not all([pickup_lat, pickup_lng, dropoff_lat, dropoff_lng]):
            return Response(
                {'detail': 'pickup_lat, pickup_lng, dropoff_lat and dropoff_lng are all required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # call Google Distance Matrix API
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        params = {
            'origins'      : f'{pickup_lat},{pickup_lng}',
            'destinations' : f'{dropoff_lat},{dropoff_lng}',
            'units'        : 'metric',
            'key'          : GOOGLE_MAPS_API_KEY,
        }

        try:
            response = requests.get(url, params=params)
            data     = response.json()

            if data['status'] != 'OK':
                return Response(
                    {'detail': 'Could not calculate distance. Check coordinates.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            element = data['rows'][0]['elements'][0]

            if element['status'] != 'OK':
                return Response(
                    {'detail': 'No route found between the two locations.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            distance_m  = element['distance']['value']   # meters
            duration_s  = element['duration']['value']   # seconds
            distance_km = distance_m / 1000
            duration_min = round(duration_s / 60)
            fare        = calculate_fare(distance_km)

            return Response({
                'pickup'        : {'lat': pickup_lat, 'lng': pickup_lng},
                'dropoff'       : {'lat': dropoff_lat, 'lng': dropoff_lng},
                'distance_km'   : round(distance_km, 2),
                'duration_min'  : duration_min,
                'estimated_fare': fare,
                'currency'      : 'GHS',
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'detail': f'Error contacting Google Maps: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )