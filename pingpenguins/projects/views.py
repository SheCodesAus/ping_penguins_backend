from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Board, Category, Note
from .serializers import BoardSerializer, CategorySerializer, NoteSerializer, BoardDetailSerializer
from .permissions import IsSuperUser, IsOwnerOrReadOnly


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
    permission_classes = [
        IsSuperUser, 
        permissions.IsAuthenticated
        ] 
    # Only auth token/logged in user can view board detail, superuser can post/edit/delete
    
    def get_object(self, code):
        try:
            board = Board.objects.get(code=code)
            self.check_object_permissions(self.request, board)
            return Board
        except Board.DoesNotExist:
            return Response({"404": "Project Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, code):
        board = self.get_object(code)
        serializer = BoardSerializer(board)
        return Response(serializer.data)
    
    def put(self, request, code):
        board = self.get_object(code)
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
    def delete(self, request, code):
        project = self.get_object(code)
        #Only Super User can delete board
        if request.user.is_superuser:
            project.delete()
            return Response({"200: Project deleted successfully"}, status=status.HTTP_200_OK)
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
    # Only a User with Auth token can view or create Notes.  SuperUser can create/edit/delete.

    def get(self, request):
        if request.user.is_superuser:
            notes = Note.objects.all()
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        else:
            return Response({"403": "Forbidden.  You are not authorised to view this content"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
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
            return Response({"404": "This Note Does Note Exist"}, status=status.HTTP_404_NOT_FOUND)
        
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
            return Response({"200: Note deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"403: Forbidden.  You are not authorised to delete this Note"}, status=status.HTTP_403_FORBIDDEN)
