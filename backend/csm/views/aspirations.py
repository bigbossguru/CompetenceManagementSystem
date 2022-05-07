from rest_framework.generics import GenericAPIView
from rest_framework.views import Response, status

from csm.serializers.aspirations import AspirationsDataSerializer
from csm.aspirations.aspirations_calculate import aspirations_calculate


class AspirationsDataCalculateView(GenericAPIView):
    serializer_class = AspirationsDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = AspirationsDataSerializer(data=request.data)
        if serializer.is_valid():
            result = aspirations_calculate(serializer.validated_data)
            return Response(data=result, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
