const authService     = require("../services/auth_services");


const authenticate_user = (req, res) => {
    const email = req.body.email;
    const password = req.body.password;

    authService.login_user(email, password, res)
    .then( response => {
      res.cookie('access_token', `${response}`, {httpOnly: false });
      res.cookie("email", `${email}`, {httpOnly: false});
      res.render("Admin/AdminMenu/menu", {
        email: email, 
        warnings: [],
        menuType: "main"
      })
    })
    .catch( error => {
        console.log("Error in login_user");
        res.render("error", {error: `Error in login_user => ${error}`});
    });
}

const logout_user = (req, res) => {
    const access_token = req.cookies.access_token;

    authService.logout_user(access_token, res)
    .then( response => {
      res.cookie('access_token', " ", {httpOnly: true });
      res.cookie("email", " ", {httpOnly: true});
      res.render("login", {message: response})
    })
    .catch( error => {
      console.log("Error in logout_user")
      res.render("error", {error: `Error in logout_user => ${error}`});
    });
}


module.exports = {
    authenticate_user,
    logout_user
}