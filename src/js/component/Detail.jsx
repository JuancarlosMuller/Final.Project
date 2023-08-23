import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useContext, useState, useEffect } from "react";
import { UserContext } from "../store/UserContext";
import { useNavigate, useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPersonHalfDress, faEye, faCalendar, faRulerVertical} from "@fortawesome/free-solid-svg-icons";


const Detail = () => {
    const { characterData } = useContext(UserContext);
    const { characterId } = useParams();
    console.log("characterId desde Params:", characterId); 

    const selectedCharacter = characterData.find(character => character.result.uid === characterId);
    const shuffledCharacters = characterData.slice().sort(() => Math.random() - 0.5);
    
    if (!selectedCharacter) {
        return <p>Loading...</p>;
    }
    return (
        <>
            <section className="py-5">
                <div className="container px-4 px-lg-5 my-5">
                    <div className="row gx-4 gx-lg-5 align-items-center">
                        <div className="col-md-6"><img className="card-img-top mb-5 mb-md-0" src="https://dummyimage.com/600x700/dee2e6/6c757d.jpg" alt="..." /></div>
                        <div className="col-md-6">
                            <div className="small mb-1">{selectedCharacter.result.description}</div>
                            <h1 className="display-5 fw-bolder">{selectedCharacter.result.properties.name}</h1>
                            <div className="fs-5 mb-5">
                                <p className="fs-4">
                                <FontAwesomeIcon icon={faPersonHalfDress} className="me-2 text-muted" />{selectedCharacter.result.properties.gender}</p>
                                <p className="fs-4">
                                <FontAwesomeIcon icon={faEye} className="me-2 text-muted" />{selectedCharacter.result.properties.eye_color}</p>
                                <p className="fs-4">
                                <FontAwesomeIcon icon={faCalendar} className="me-2 text-muted" />{selectedCharacter.result.properties.birth_year}</p>
                                <p className="fs-4">
                                <FontAwesomeIcon icon={faRulerVertical} className="me-2 text-muted" />{selectedCharacter.result.properties.height}</p>
                            </div>
                            <p className="lead">Lorem ipsum dolor sit amet consectetur adipisicing elit. Praesentium at dolorem quidem modi. Nam sequi consequatur obcaecati excepturi alias magni, accusamus eius blanditiis delectus ipsam minima ea iste laborum vero</p>
                            <div className="d-flex">

                                <button className="btn btn-outline-dark flex-shrink-0" type="button">
                                    <i className="bi-cart-fill me-1"></i>
                                    Add to cart
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="py-5 bg-light">
                <div className="container px-4 px-lg-5 mt-5">
                    <h2 className="fw-bolder mb-4">Related products</h2>

                    <div className="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center">
                        {shuffledCharacters.slice(0, 4).map(character => (
                            <div className="col mb-5" key={character.result.uid}>
                                <div className="card h-100">

                                    <img className="card-img-top" src="https://dummyimage.com/450x300/dee2e6/6c757d.jpg" alt="..." />

                                    <div className="card-body p-4">
                                        <div className="text-center">

                                            <h5 className="fw-bolder">{character.result.properties.name}</h5>

                                            {character.result.properties.gender}
                                        </div>
                                    </div>

                                    <div className="card-footer p-4 pt-0 border-top-0 bg-transparent">
                                        <div className="text-center">
                                            <Link to={`/detail/${character.result.uid}`} className="btn btn-outline-dark mt-auto">View options</Link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </>
    )
};

export default Detail;