

const get_mainMenu = (req, res) => {
    const email = req.cookies.email;

    try {
        res.render("./Admin/AdminMenu/menu", {
            email: email, 
            warnings: [],
            menuType: "main"
        });
    } catch (error) {
        console.log("Error in get_mainMenu, CONTROLLERS/menu_controllers")
        res.redirect("back")
    }
}

const get_settingsMenu = (req, res) => {
    const email = req.cookies.email;

    try {
        res.render("./Admin/AdminMenu/menu", {
            email: email, 
            warnings: [],
            menuType: "settings"
        });
    } catch (error) {
        console.log("Error in get_settingsMenu, CONTROLLERS/menu_controllers")
        res.redirect("back")
    }
}

const get_reportsMenu = (req, res) => {
    const email = req.cookies.email;

    try {
        res.render("./Admin/AdminMenu/menu", {
            email: email, 
            warnings: [],
            menuType: "reports"
        });
    } catch (error) {
        console.log("Error in get_reportsMenu, CONTROLLERS/menu_controllers")
        res.redirect("back")
    }
}


module.exports = {
    get_mainMenu,
    get_reportsMenu,
    get_settingsMenu
}
