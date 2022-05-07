const express   = require("express");
const auth_controllers = require("../controllers/auth_controllers");

const router    = express.Router();

router.post("/login", auth_controllers.authenticate_user);
router.get("/logout", auth_controllers.logout_user);

module.exports = router;