from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pokemon
from .serializers import PokemonSerializer


def unauthorized():
    return Response(
        {'detail': 'Authentication credentials were not provided.'},
        status=status.HTTP_401_UNAUTHORIZED,
    )


class PokemonListCreateAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return unauthorized()

        pokemons = Pokemon.objects.all().order_by('id')
        serializer = PokemonSerializer(pokemons, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return unauthorized()

        serializer = PokemonSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PokemonRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return unauthorized()

        pokemon = Pokemon.objects.filter(pk=pk).first()

        if pokemon is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PokemonSerializer(pokemon, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        if not request.user.is_authenticated:
            return unauthorized()

        pokemon = Pokemon.objects.filter(pk=pk).first()

        if pokemon is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PokemonSerializer(
            pokemon, data=request.data, partial=True, context={'request': request}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return unauthorized()

        pokemon = Pokemon.objects.filter(pk=pk).first()

        if pokemon is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        pokemon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
