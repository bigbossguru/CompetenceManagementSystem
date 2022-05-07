const system            = require("../services/system_services");


const get_setup = async(req, res) => {
    const email = req.cookies.email;
    const access_token = req.cookies.access_token;

    try {
        const exportList = await system.get_exportList(access_token);

        res.render("./Admin/Settings/SystemParams/systemParams", {
            email: email, 
            warnings: [],
            exports: exportList
        });
    } catch (error) {
        console.log("Error in get_setup, CONTROLLERS/settings_controllers")
        res.redirect("back")
    }
}

const get_weights = async(req, res) => {
    const email = req.cookies.email;
    const access_token = req.cookies.access_token;

    try {
        const aaData = await system.get_aaCompetenceList(access_token);
        const rdData = await system.get_rdCompetenceList(access_token);

        res.render("./Admin/Settings/CompWeights/compWeights", {
            email: email, 
            warnings: [],
            rdData: rdData,
            aaData: aaData
        });
    } catch (error) {
        console.log("Error in get_weights, CONTROLLERS/settings_controllers")
        res.redirect("back")
    }
}

const set_weights = async(req, res) => {
    const access_token = req.cookies.access_token;
    var type = "";
    var inputWeights = req.body;
    
    try {
        if(inputWeights["rdTable_length"]){
            delete inputWeights["rdTable_length"]
            type = "rd"
        } else if (inputWeights["aaTable_length"]){
            delete inputWeights["aaTable_length"]
            type = "aa"
        }
    
        await system.set_default_weights(access_token, inputWeights, type)

        res.redirect("back")
    } catch (error) {
        console.log("Error in set_weights, CONTROLLERS/settings_controllers")
        res.redirect("back")
    }
}

module.exports = {
    get_setup,
    get_weights,
    set_weights
}