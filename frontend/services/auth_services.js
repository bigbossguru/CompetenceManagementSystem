const axios         = require("axios");


const login_user = (email, password) => {
    return axios.post('http://localhost:8000/api/v1/auth/login/', {
    email: email,
    password: password
    })
    .then( response => {
        return response.data.access_token
    })
    .catch( error => {
        console.log("Error in login_user");
        res.render("error", {error: `Error in login_user => ${error}`});
        return error
    });
}

const logout_user = (access_token) => {
    return axios.post(`${process.env.API_URL_BASE}/auth/logout/`, {
        headers: {
          Authorization: 'JWT ' + access_token
        }
      })
      .then( response => {
        return response.data.detail
      })
      .catch( error => {
        console.log("Error in logout_user")
        res.render("error", {error: `Error in logout_user => ${error}`});
        return error
      });
}

module.exports = {
    login_user,
    logout_user
}