const isLoggedIn = (req, res, next) => {
    if (req.cookies.access_token === " " || req.cookies.access_token === undefined){
        res.redirect("/");
    } else {
        next()
    }
}

module.exports = {
    isLoggedIn
}