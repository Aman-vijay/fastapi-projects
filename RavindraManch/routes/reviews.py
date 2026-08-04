from fastapi import APIRouter,Depends,Query,HTTPException
from models import Review,ReviewCreate,ReviewRead,ReviewUpdate
from sqlmodel import Session,select,func
from db import get_session


router = APIRouter(prefix="/review",tags=["reviews"])



@router.post("/",response_model=ReviewRead)
def create_reviews(review:ReviewCreate,session:Session = Depends(get_session)):
    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


@router.get("/",response_model=list[ReviewRead])
def list_reviews( 
    play_name: str | None = Query(None,description="Filter by play name"), 
    skip:int =  Query(0,ge=0,description="Offset for the review"),
    limit:int = Query(10,ge=1,le=50,description="Max reviews per req"),
    session:Session =  Depends(get_session)
):
    query = select(Review)
    if play_name:
        query = query.where(Review.play_name ==play_name)

    query=query.offset(skip).limit(limit)
    reviews = session.exec(query).all()

    return reviews

@router.get("/avg/{play_name}")
def get_avg_ratings(
    play_name = str,
    session:Session =  Depends(get_session)
):
    ratings = session.exec(
        select( 
            func.avg(Review.rating),func.count(Review.id)
        ).where(
            Review.play_name == play_name
        )
    ).first()

    avg_rating,total_reviews = ratings

    if total_reviews == 0:
        raise HTTPException(status_code=404,detail="No events found")

    return{
        "play_name":play_name,
        "average_ratings":round(avg_rating,2),
        "total_reviews":total_reviews
    }    


@router.get("/{id}",response_model=ReviewRead)
def get_review_by_id(id:int,session:Session=Depends(get_session)):
    review = session.get(Review,id)

    if not review:
        raise HTTPException(status_code=404,detail="No such play")

    return review

@router.patch("/{id}",response_model=ReviewRead)
def update_review_by_id(id:int,update:ReviewUpdate,session:Session=Depends(get_session)):
    review = session.get(Review,id)

    if not review:
        raise HTTPException(status_code=404,detail="No such play")
        
    update_data = update.model_dump(exclude_unset = True)
    for key,value in update_data.items():
        setattr(review,key,value)

    session.add(review)
    session.commit() 
    session.refresh(review)
    return review  

@router.delete("/{id}")
def delete_review_by_id(id:int,session:Session=Depends(get_session)):
    review = session.get(Review,id)

    if not review:
        raise HTTPException(status_code=404,detail="No such play")
        

    session.delete(review)
    session.commit() 

    return {"message":"Your review has been deleted"}    



