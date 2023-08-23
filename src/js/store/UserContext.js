import React, { createContext, useEffect, useState } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [userData, setUserData] = useState([]);
  const [charactersData, setCharactersData] = useState([]);
const [characterData, setCharacterData] = useState([]);

  const getCharacters = () => {
    const url = "https://www.swapi.tech/api/people/";

    const getOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    };
    fetch(url, getOptions)
      .then(getResponse => {
        if (getResponse.status >= 200 && getResponse.status < 300) {
          console.log("GET: Characters cargados exitosamente");
          return getResponse.json();
        } else {
          console.log(`Error en la solicitud GET ${getResponse.status}`);
        }
      })
      .then(data => {
        if (Array.isArray(data.results)) {
          console.log("Data obtenida de la primera llamada GET:", data);
          setCharactersData(data.results);

          // Realizar llamadas GET para cada URL de personaje
          const characterUrls = data.results.map(character => character.url);
          const characterPromises = characterUrls.map(characterUrl =>
            fetch(characterUrl, getOptions)
              .then(characterResponse => {
                if (characterResponse.status >= 200 && characterResponse.status < 300) {
                  return characterResponse.json();
                } else {
                  console.log(`Error en la solicitud GET ${characterResponse.status}`);
                  throw new Error("Error en la solicitud GET");
                }
              })
          );

          // Procesar los resultados de las llamadas GET individuales
          Promise.all(characterPromises)
            .then(characterDataArray => {
              console.log("Detalles de los personajes:", characterDataArray);
              // Almacenar la información de los personajes en el estado characterData
              setCharacterData(characterDataArray);
            })
            .catch(error => {
              console.error("Error en la solicitud GET:", error);
            });
        } else {
          console.log("Error: Data.results no es un array.");
        }
      })
      .catch(error => {
        console.error("Error en la solicitud GET:", error);
      });
  };






  const getagenda = () => {
    const url = "https://playground.4geeks.com/apis/fake/contact/agenda/juana";

    const getOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    };
    fetch(url, getOptions)
      .then(getResponse => {
        if (getResponse.status >= 200 && getResponse.status < 300) {
          console.log("GET: Agenda cargada exitosamente");
          return getResponse.json();
        } else {
          console.log(`Error en la solicitud GET ${getResponse.status}`);
        }
      })
      .then(data => {
        setUserData(data);
      })
      .catch(error => {
        console.error("Error en la solicitud GET:", error);
      });
  };

  const updateUserContact = (updatedContact) => {
    console.log("userData actualizado en contexto:", updatedContact);
    const updatedUserData = userData.map(contact =>
      contact.id === updatedContact.id ? updatedContact : contact
    );
    setUserData(updatedUserData);
  };

  const addNewUserContact = (newContact) => {

    setUserData([...userData, newContact]);
  };

  return (
    <UserContext.Provider value={{ charactersData, setCharactersData, getCharacters, characterData, setCharacterData, userData, setUserData, updateUserContact, addNewUserContact, getagenda }}>
      {children}
    </UserContext.Provider>
  );
};
