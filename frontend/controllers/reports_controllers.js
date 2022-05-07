const empService    = require("../services/employees_services");


const get_overview = async(req, res) => {
    const email         = req.cookies.email;
    const access_token  = req.cookies.access_token;

    const aaCompetenceList  = await empService.get_AAcompetence_list(access_token)
    const rdCompetenceList  = await empService.get_RDcompetence_list(access_token)
    const metierFields      = await empService.get_metierFields_list(access_token)
    const platforms         = await empService.get_platforms_list(access_token)

    empService.get_employee_list(access_token)
    .then( employeeList => { 
      res.render("./Admin/Reports/Overview/overview", {
        email: email, 
        warnings: [],
        data: employeeList,
        aaCompetenceList: aaCompetenceList,
        rdCompetenceList: rdCompetenceList,
        metierfields: metierFields,
        platforms: platforms
      });
     })
    .catch( error => {
      console.log("Error in get_overview" + error)
      res.render("error", {error: `Error in get_overview => ${error}`});
    })
}

const get_overview_detail = async(req, res) => {
  const email         = req.cookies.email;
  const access_token  = req.cookies.access_token;
  const ps_id         = req.params.ps_id;

  const aaDetail      = await empService.get_AAcompetence_detail(access_token, ps_id);
  const rdDetail      = await empService.get_RDcompetence_detail(access_token, ps_id);
  const empDetail     = await empService.get_employee_detail(access_token, ps_id);


  const generalInfo     = [
    "Drive performance", 
    "Be Agile", 
    "Speak with facts and data", 
    "Promote collaborative attitude", 
    "Focus on Customer", 
    "Innovate"
  ];

  const managementInfo  = [
    "Inspire & Engage Teams", 
    "Think Strategy", 
    "Build & Develop Effective Teams", 
    "Act with Managerial Courage"
  ];

  const softSkillsInfo  = [
    "Product Standard", 
    "Technical training", 
    "Creativity", 
    "Product Road Map", 
    "Automotive expertise", 
    "Development Process", 
    "Process,Methods & Tools", 
    "Technical skills" 
  ];

  var managementResult  = matchAndSort(managementInfo, aaDetail);
  var generalResult     = matchAndSort(generalInfo, aaDetail);
  var softSkillsResult  = matchAndSort(softSkillsInfo, aaDetail);

  rdResults = [];
  rdDetail.forEach( competence => {
    if(competence){
      rdResults.push({
      name: competence.competence.name,
      reqLevel: competence.expected_lvl,
      rating: competence.acquired_lvl,
      weight: competence.competence.weight
    })
    }
  })

  res.render("./Admin/Reports/Overview/overviewDetail", {
    email: email, 
    warnings: [],
    data: empDetail,
    generalComp: generalResult,
    managementComp: managementResult,
    softSkills: softSkillsResult,
    rdResults: rdResults
  });
}

const filter_employees = async (req, res) => {
  const email             = req.cookies.email;
  const access_token      = req.cookies.access_token;
  const query             = req.body;

  const aaCompetenceList  = await empService.get_AAcompetence_list(access_token)
  const rdCompetenceList  = await empService.get_RDcompetence_list(access_token)
  const metierFields      = await empService.get_metierFields_list(access_token)
  const platforms         = await empService.get_platforms_list(access_token)

  empService.get_filtered_employee_list(access_token, query)
    .then( data => { 
      res.render("./Admin/Reports/Overview/overview", {
        email: email, 
        warnings: [],
        data: data,
        aaCompetenceList: aaCompetenceList,
        rdCompetenceList: rdCompetenceList,
        metierfields: metierFields,
        platforms: platforms
      });
     })
    .catch( error => {
      console.log("Error in get_overview" + error)
      res.render("error", {error: `Error in get_overview => ${error}`});
    })
    }

const get_aspiration = (req, res) => {
  const email = req.cookies.email;
 
  res.render("./Admin/Reports/Aspiration/aspiration", {
    email: email, 
    warnings: [],
    data: []
  });
}

const get_aspiration_employee = async (req, res) => {
  const email         = req.cookies.email;
  const access_token  = req.cookies.access_token;
  const ps_id         = req.body.ps_id;

  const data          = await empService.get_employee_detail(access_token, ps_id);
  const aaCompetence  = await empService.get_AAcompetence_detail(access_token, ps_id);
  const rdCompetence  = await empService.get_RDcompetence_detail(access_token, ps_id);

  //Gets just needed data from rdCompetence Array
  var rdData = [];
  if(rdCompetence.length){
    rdCompetence.forEach( competence => {
      rdData.push({
        name: competence.competence.name,
        rating: competence.acquired_lvl,
        weight: competence.competence.weight,
        id: competence.competence.competence_id
      })
    })
  }

  //Gets just needed data from aaCompetence Array
  var aaData = [];
  if(aaCompetence.length){
    aaCompetence.forEach( competence => {
      aaData.push({
        name: competence.competence.name,
        requiredLvl: competence.expected_lvl,
        rating: competence.rating,
        weight: competence.competence.weight,
        code: competence.competence.code
      })
    })
  }
  
  var result            = [];
  var ids               = [];
  var weights           = [];
  var competence_weight = [];

  for(var i in req.body){
    result.push([i, req.body [i]]);
  }
  result.forEach( item => {
    ids.push(item[0]);
    weights.push(item[1]);  
  })

  for (let i = 0; i < ids.length - 1; i++){
    if(ids[i] === "ps_id"){
      continue
    } else {
      var obj = {
        competence_id: ids[i],
        weight: weights[i]
      }
      competence_weight.push(obj);
    }
  }

  const candidates = await empService.get_aspirationCandidates(access_token, ps_id, competence_weight);
  if (candidates.message === "not found" ){
    res.render("./Admin/Reports/Aspiration/aspiration", {
      email: email, 
      warnings: ["Match not found!"],
      data: []
    });
  } else {
    await res.render("./Admin/Reports/Aspiration/aspiration", {
      email: email, 
      warnings: [],
      data: data,
      aaData: aaData,
      rdData: rdData,
      candidates: candidates
    });
  }
  
}

const get_aspiration_detail = async(req, res) => {
    const email           = req.cookies.email;
    const access_token    = req.cookies.access_token;
    const ps_id           = req.params.ps_id;
  
    const aaDetail        = await empService.get_AAcompetence_detail(access_token, ps_id);
    const rdDetail        = await empService.get_RDcompetence_detail(access_token, ps_id);
    const empDetail       = await empService.get_employee_detail(access_token, ps_id);
  
  
    const generalInfo     = [
      "Drive performance", 
      "Be Agile", 
      "Speak with facts and data", 
      "Promote collaborative attitude", 
      "Focus on Customer", 
      "Innovate"
    ];

    const managementInfo  = [
      "Inspire & Engage Teams", 
      "Think Strategy", 
      "Build & Develop Effective Teams", 
      "Act with Managerial Courage"
    ];

    const softSkillsInfo  = [
      "Product Standard", 
      "Technical training", 
      "Creativity", 
      "Product Road Map", 
      "Automotive expertise", 
      "Development Process", 
      "Process,Methods & Tools", 
      "Technical skills"
    ];

    var managementResult  = matchAndSort(managementInfo, aaDetail);
    var generalResult     = matchAndSort(generalInfo, aaDetail);
    var softSkillsResult  = matchAndSort(softSkillsInfo, aaDetail);
  
    rdResults = [];
    rdDetail.forEach( competence => {
      if(competence){
        rdResults.push({
        name: competence.competence.name,
        reqLevel: competence.expected_lvl,
        rating: competence.acquired_lvl,
        weight: competence.competence.weight
      })
      }
    })
  
    res.render("./Admin/Reports/Aspiration/aspirationDetail", {
      email: email, 
      warnings: [],
      data: empDetail,
      generalComp: generalResult,
      managementComp: managementResult,
      softSkills: softSkillsResult,
      rdResults: rdResults
    });
}

const get_stagnation = (req, res) => {
  
}

const get_stagnation_detail = (req, res) => {
  
}



//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//%%%%%%%%        PRIVATE FUNCTIONS       %%%%%%%%%%%%%%%%%%%%%%%%%
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

const matchAndSort = (arrayToMatch, matchedArray) => {
  var generalResult = [];

  arrayToMatch.forEach((competence) => {
    data = matchedArray.find( (post, index) => {
      if(post.competence.name == competence)
        return { index };
    });
    if (data){
      generalResult.push({
        name: data.competence.name,
        reqLevel: data.expected_lvl,
        rating: data.rating
      })
    }
  });

  return generalResult
}



module.exports = {
    get_overview,
    get_aspiration,
    get_stagnation,
    get_overview_detail,
    get_aspiration_employee,
    get_stagnation_detail,
    filter_employees,
    get_aspiration_detail
}