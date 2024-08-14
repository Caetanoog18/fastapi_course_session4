from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course_model import CourseModel
from schemas.course_schemas import CourseSchema
from core.deps import get_session

router = APIRouter()

# POST course
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def post_course(course: CourseSchema, db: AsyncSession = Depends(get_session)):
    new_course = CourseModel(title=course.title, classes=course.classes, duration=course.duration)

    db.add(new_course)
    await db.commit()

    return new_course

# GET courses
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CourseSchema])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        '''
        Cria uma consulta SQLAlchemy que seleciona todas as colunas da tabela representada pelo modelo 
        CourseModel. O CourseModel é provavelmente uma classe SQLAlchemy que mapeia uma tabela do banco 
        de dados.
        '''
        query = select(CourseModel)
        '''
        Executa a consulta SQL de forma assíncrona na sessão de banco de dados e armazena o resultado na 
        variável result. Como a execução da consulta é um processo de I/O, ela é aguardada com await.
        '''
        result = await session.execute(query)
        '''
        result.scalars(): Extrai todas as colunas ou escalas retornadas pela consulta 
        (neste caso, instâncias de CourseModel).

        .all(): Retorna todos os resultados da consulta como uma lista.

        courses: List[CourseModel]: Declara explicitamente que courses é uma lista de 
        objetos do tipo CourseModel
        '''
        courses: List[CourseModel] = result.scalars().all()

        return  courses
    
# GET course
@router.get('/{course_id}', status_code=status.HTTP_200_OK, response_model=CourseSchema)
async def get_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(detail="Course was not found", status_code=status.HTTP_404_NOT_FOUND)
        
# PUT course
@router.put('/{course_id}', status_code=status.HTTP_202_ACCEPTED, response_model=CourseSchema)
async def put_course(course_id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_up = result.scalar_one_or_none()

        if course_up:

            course_up.title = course.title
            course_up.classes = course.classes
            course_up.duration = course.duration

            await session.commit()

            return course_up
        
        else:
            raise HTTPException(detail="Course was not found", status_code=status.HTTP_404_NOT_FOUND)
        
# DELETE course
@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_del = result.scalar_one_or_none()

        if course_del:
            await session.delete(course_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(detail="Course was not found", status_code=status.HTTP_404_NOT_FOUND)

