from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Board, Category, Note
from .serializers import BoardSerializer, CategorySerializer, NoteSerializer, BoardDetailSerializer
from .permissions import IsSuperUser, IsOwnerOrReadOnly, IsAuthenticatedReadOnly


class BoardList(APIView):
    permission_classes = [IsSuperUser] 
    # Only SuperUser can view Board List and post a board

    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class BoardDetail(APIView):
    # permission_classes = [IsAuthenticatedReadOnly] 
    # Only auth token/logged in user can view board detail, superuser can post/edit/delete
    
    def get_object(self, pk):
        try:
            board = Board.objects.get(pk=pk)
            self.check_object_permissions(self.request, board)
            return board
        except Board.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)
    
    def put(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardDetailSerializer(
            instance=board,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, pk):
        project = self.get_object(pk)
        #Only Super User can delete board
        if request.user.is_superuser:
            project.delete()
            return Response({"202: Project deleted successfully"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"403: Forbidden.  You are not authorised to delete this Project"}, status=status.HTTP_403_FORBIDDEN)


class CategoryList(APIView):
    permission_classes = [IsSuperUser] 
    # Only SuperUser can post Category and post a Category (while posting board)  

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class NoteList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(owner=request.user)  # Filter notes by authenticated user
        category_id = request.query_params.get('category')  # Optional category filter
        if category_id:
            notes = notes.filter(category_id=category_id)

        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['owner'] = request.user.id

        category_id = data.get("category")
        if not category_id:
            return Response(
                {"error": "Category ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NoteDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        
    def get_object(self, pk):
        try:
            note = Note.objects.get(pk=pk)
            self.check_object_permissions(self.request, note)
            return note
        except Note.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, context={'request': request}) # This context is required for the method that determines anonymous permissions in the serializers is applicable
        return Response(serializer.data)
    
    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteSerializer(instance=note,data=request.data,partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        note = self.get_object(pk)
        #Only Super Users can delete
        if request.user.is_superuser:
            note.delete()
            return Response({"202: Note deleted successfully"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"403: Forbidden.  You are not authorised to delete this Note"}, status=status.HTTP_403_FORBIDDEN)

class BoardNotes(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404

        notes = Note.objects.filter(category__board=board)
        
        # filter by category as well
        category_id = request.query_params.get('category')
        if category_id:
            notes = notes.filter(category_id=category_id)

        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)