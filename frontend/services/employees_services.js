const axios         = require("axios");
const { attachment } = require("express/lib/response");
require("dotenv").config();
var FormData = require('form-data');


//LISTS
const get_employee_list = (access_token) => {
      
    return axios.get(`${process.env.API_URL_BASE}/employee/`, {
      headers: {
        Authorization: 'JWT ' + access_token
      }
    })
    .then( result => {
      return result.data.results
    })
    .catch( error => {
      console.log("Error in get_employee_list, SERVICES/employees_services")
      return error
    })
}

const get_filtered_employee_list = (access_token, query) => {
    if(query.aacompetence === undefined){
      query.aacompetence = "";
    }

    const params = {
      ps_id: query.psID,
      first_name: query.firstName,
      last_name: query.lastName.toUpperCase(),
      location: query.location,
      orgaloc: query.orgaloc,
      hn1__first_name: query.hn1,
      hn2__first_name: query.hn2,
      job__metier_field: query.metierfield,
      aa_employees__competence__name: query.aacompetence,
      rd_employees__competence__name: query.rdcompName,
      rd_employees__competence__type: query.compType,
      rd_employees__competence__metier_org: query.compMetier,
      rd_employees__competence__category: query.compCategory,
      rd_employees__competence__domain: query.compDomain
    }
    
    return axios.get(`${process.env.API_URL_BASE}/employee/`, {
      params: params,
      headers: {
        Authorization: 'JWT ' + access_token
      }
    })
    .then(result => {
      return result.data.results
    })
    .catch(error => {
      console.log("Error in get_filtered_employee_list, SERVICES/employees_services")
      return error
    })
}

const get_RDcompetence_list = async(access_token) => {
  const propertyList = await get_RDcompetence_propertyList(access_token);
  return sort_RDcompetence_list(propertyList);
}

const get_AAcompetence_list = async(access_token) => {
  const propertyList = await get_AAcompetence_propertyList(access_token);
  return sort_competence_list(propertyList);
}

const get_metierFields_list = async(access_token) => {
  const propertyList = await get_metieFields_propertyList(access_token);
  return sort_competence_list(propertyList);
}

const get_platforms_list = async(access_token) => {
  const propertyList = await get_platforms_propertyList(access_token);
  return sort_competence_list(propertyList);
}

//DETAILS
const get_employee_detail = (access_token, ps_id) => {
  return axios.get(`${process.env.API_URL_BASE}/employee/`, {
    params: {
      ps_id: `${ps_id}`
    },
    headers: {
      Authorization: 'JWT ' + access_token
    }
  })
  .then(detail => {
    return detail.data.results[0]
  })
  .catch(error => {
    console.log("Error in get_employee_detail, SERVICES/employees_services")
    return error
  })
}


const get_AAcompetence_detail = (access_token, ps_id) => {

    return axios.get(`${process.env.API_URL_BASE}/employee/aacompetence/`, {
      params: {
        employee__ps_id: `${ps_id}`
      },
      headers: {
        Authorization: 'JWT ' + access_token
      }
    })
    .then(detail => {
      return detail.data.results
    })
    .catch(error => {
      console.log("Error in get_AAcompetence_detail, SERVICES/employees_services")
      return error
    })     
}

const get_RDcompetence_detail = (access_token, ps_id) => {

    return axios.get(`${process.env.API_URL_BASE}/employee/rdcompetence/`, {
        params: {
          employee__ps_id: `${ps_id}`
      },
        headers: {
          Authorization: 'JWT ' + access_token
        }
      })
      .then(detail => {
        return detail.data.results
      })
      .catch(error => {
        console.log("Error in get_RDcompetence_detail, SERVICES/employees_services")
      })
}


const get_aspirationCandidates = (access_token, ps_id, competenceWeights) => {
  const psid = parseInt(ps_id);
  return axios.post(`${process.env.API_URL_BASE}/aspirations/`, 
  {
    "subject": {
      "ps_id": psid,
    },
    "competence_weight": competenceWeights
  },
  {
    headers: {
      'content-type': 'application/json',
      Authorization: 'JWT ' + access_token
    }
  }
  )
  .then(response => {
    return response.data.results
  })
  .catch((error) => {
    console.log("Error in get_aspirationCandidates, SERVICES/employees_services")
  })

}

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// %%%%%%%%%%%%     PRIVATE FUNCTIONS     %%%%%%%%%%%%%%%%%%%%%%%

const sort_RDcompetence_list = (list) => {
        var rdCompetenceList = [];
        var types = [];
        var categories = [];
        var domains = [];
        var names = [];
        var metiers = [];

        list.forEach(element => {
          types.push(element.type);
          categories.push(element.category);
          domains.push(element.domain);
          names.push(element.name);
          metiers.push(element.metier_org);
        });

        let uniqueNames = names.filter((element, index) => {
          return names.indexOf(element) === index;
        });
        let uniqueCategories = categories.filter((element, index) => {
          return categories.indexOf(element) === index;
        });
        let uniqueDomains = domains.filter((element, index) => {
          return domains.indexOf(element) === index;
        });
        let uniqueMetiers = metiers.filter((element, index) => {
          return metiers.indexOf(element) === index;
        });
        let uniqueTypes = types.filter((element, index) => {
          return types.indexOf(element) === index;
        });

        rdCompetenceList = {
          types: uniqueTypes,
          categories: uniqueCategories,
          domains: uniqueDomains,
          names: uniqueNames,
          metiers: uniqueMetiers
        }
        
        return rdCompetenceList;
}

const sort_competence_list = (list) => {
  var competenceList = [];
      
  list.forEach(element => {
    competenceList.push(element.name);
  });
  return competenceList
}

const get_RDcompetence_propertyList = (access_token) => {
  return axios.get(`${process.env.API_URL_BASE}/rdcompetence/?limit=1000000`, {
    headers: {
      Authorization: 'JWT ' + access_token
    }
  })
  .then(list => {
      return list.data.results
    })
  .catch(error => {
    
    return error
  })
}

const get_AAcompetence_propertyList = (access_token) => {
  return axios.get(`${process.env.API_URL_BASE}/aacompetence/?limit=1000000`, {
    headers: {
      Authorization: 'JWT ' + access_token
    }
  })
  .then(list => {
      return list.data.results;
    })
  .catch(error => {

    return error
  })
}

const get_metieFields_propertyList = (access_token) => {
  return axios.get(`${process.env.API_URL_BASE}/rdcompetence/metierfield`, {
    headers: {
      Authorization: 'JWT ' + access_token
    }
  })
  .then(list => {
    return list.data.results;
    })
  .catch(error => {

    return error
  })
}

const get_platforms_propertyList = (access_token) => {
  return axios.get(`${process.env.API_URL_BASE}/rdcompetence/platform`, {
    headers: {
      Authorization: 'JWT ' + access_token
    }
  })
  .then(list => {
      return list.data.results;
    })
  .catch(error => {

    return error
  })
}


module.exports = {
    get_employee_list,
    get_RDcompetence_list,
    get_AAcompetence_list,
    get_employee_detail,
    get_AAcompetence_detail,
    get_RDcompetence_detail,
    get_filtered_employee_list,
    get_metierFields_list,
    get_platforms_list,
    get_aspirationCandidates
}