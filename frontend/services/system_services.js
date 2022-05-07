const axios             = require("axios");
require("dotenv").config();


//LISTS
const get_exportList = (access_token) => {
      
    return axios.get(`${process.env.API_URL_BASE}/system/config/files/`, {
      headers: {
        Authorization: 'JWT ' + access_token
      }
    })
    .then(response => {
        return response.data.results;
      })
    .catch(error => {
      console.log("Error in get_exportList, SERVICES/system_services")
      return error
    })  
}

const get_aaCompetenceList = (access_token) => {
  return axios.get(`${process.env.API_URL_BASE}/aacompetence/?limit=1000`, {
    headers: {
      Authorization: 'JWT ' + access_token
    }
  })
  .then(list => {
      return list.data.results;
    })
  .catch(error => {
      console.log("Error in get_aaCompetenceList, SERVICES/system_services")
      return error
  })   
}

const get_rdCompetenceList = (access_token) => {
  return axios.get(`${process.env.API_URL_BASE}/rdcompetence/?limit=1000`, {
    headers: {
      Authorization: 'JWT ' + access_token
    }
  })
  .then(list => {
      return list.data.results;
    })
  .catch(error => {
      console.log("Error in get_rdCompetenceList, SERVICES/system_services")
      return error
    })   
}

const set_default_weights = (access_token, weights, type) => {
  var weightsObjArray = [];
  const weightsKeyObjArray = Object.entries(weights);

  if(type === "aa"){
    weightsKeyObjArray.forEach( item => {
      obj = {
        code: item[0],
        weight: item[1]
      }
      weightsObjArray.push(obj);
    })
  } else if(type === "rd"){
    weightsKeyObjArray.forEach( item => {
      obj = {
        competence_id: item[0],
        weight: item[1]
      }
      weightsObjArray.push(obj);
    })
  }
  
  if (type === "aa"){
    return axios.put(`${process.env.API_URL_BASE}/aacompetence/weight/`,
     weightsObjArray
    ,{
    headers: {
      Authorization: 'JWT ' + access_token
    }
    })
    .then(response => {
      return response.data
    })
    .catch(error => {
      console.log("Error in get_aaCompetenceList, SERVICES/system_services")
      return error
    }) 
  } else if (type === "rd"){
    return axios.put(`${process.env.API_URL_BASE}/rdcompetence/weight/`,
     weightsObjArray
    ,{
    headers: {
      Authorization: 'JWT ' + access_token
    }
    })
    .then(response => {
      return response.data
    })
    .catch(error => {
      console.log("Error in get_rdCompetenceList, SERVICES/system_services")
      return error
    }) 
  }
}

module.exports = {
    get_exportList,
    get_aaCompetenceList,
    get_rdCompetenceList,
    set_default_weights
}
