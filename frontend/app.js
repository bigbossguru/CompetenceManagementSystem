const express       = require("express");
const path          = require("path");
const cookieParser  = require("cookie-parser");
const security      = require("./security/secure_functions");
const fileUpload    = require("express-fileupload");

//Routes
const authentication_routes = require("./routes/authentication_routes");
const menu_routes           = require("./routes/menu_routes");
const reports_routes        = require("./routes/report_routes");
const settings_routes       = require("./routes/settings_routes");
const error_routes          = require("./routes/error_routes");

const app = express();

//Start server
app.listen("3000", () => {
  console.log("Listening on port 3000...");
});

//Public folder
app.use("/static", express.static(__dirname + '/public'));

//JSON handler
app.use(express.urlencoded({ extended: false}));
app.use(express.json());

//Cookie Handler
app.use(cookieParser());

//File upload
//app.use(fileUpload());

//View Engine
app.set("view engine", "ejs");
app.set('views', path.join(__dirname, './views'));

//Base route
app.get("/", (req, res) => {
    res.render("logIn", {message: ""});
});

//App Main Routes
app.use("/auth", authentication_routes);
app.all("/*", security.isLoggedIn, (req, res, next) => {
  next();
})
app.use("/menu", menu_routes);
app.use("/reports", reports_routes);
app.use("/settings", settings_routes);
app.use("/error", error_routes);