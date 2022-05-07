
const handle_error_message = (req, res) => {
    errorObj = req.body;
    console.log(errorObj);
    res.redirect("/menu");
}

module.exports = {
    handle_error_message
}