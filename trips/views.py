from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project, Place
from .serializers import ProjectSerializer, ProjectCreateSerializer, PlaceSerializer
from .services import validate_artwork_exists, get_artwork


# PROJECT VIEWS

@api_view(['GET', 'POST'])
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            place_ids = serializer.validated_data.pop('places', [])
            project = Project.objects.create(**serializer.validated_data)

            for external_id in place_ids:
                artwork = get_artwork(external_id)
                if artwork:
                    Place.objects.create(
                        project=project,
                        external_id=str(external_id),
                        title=artwork.get('title', 'Unknown')
                    )

            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProjectCreateSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data.pop('places', None)
            serializer.save()
            return Response(ProjectSerializer(project).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if project.places.filter(visited=True).exists():
            return Response(
                {'error': 'Cannot delete project with visited places'},
                status=status.HTTP_400_BAD_REQUEST
            )
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# PLACE VIEWS

@api_view(['GET', 'POST'])
def place_list(request, project_pk):
    try:
        project = Project.objects.get(pk=project_pk)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        places = project.places.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if project.places.count() >= 10:
            return Response(
                {'error': 'Maximum 10 places per project'},
                status=status.HTTP_400_BAD_REQUEST
            )

        external_id = request.data.get('external_id')
        if not external_id:
            return Response({'error': 'external_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if project.places.filter(external_id=str(external_id)).exists():
            return Response(
                {'error': 'Place already exists in this project'},
                status=status.HTTP_400_BAD_REQUEST
            )

        artwork = get_artwork(external_id)
        if not artwork:
            return Response(
                {'error': 'Place not found in Art Institute API'},
                status=status.HTTP_404_NOT_FOUND
            )

        place = Place.objects.create(
            project=project,
            external_id=str(external_id),
            title=artwork.get('title', 'Unknown')
        )
        return Response(PlaceSerializer(place).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
def place_detail(request, project_pk, place_pk):
    try:
        project = Project.objects.get(pk=project_pk)
        place = project.places.get(pk=place_pk)
    except (Project.DoesNotExist, Place.DoesNotExist):
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PlaceSerializer(place, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)