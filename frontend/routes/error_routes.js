const express                   = require("express");
const error_controllers         = require("../controllers/error_controllers");

const router            = express.Router();

router.post("/", error_controllers.handle_error_message);

module.exports = router;