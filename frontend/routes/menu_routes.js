const express               = require("express");
const menu_controllers      = require("../controllers/menu_controllers");

const router            = express.Router();

router.get("/", menu_controllers.get_mainMenu);
router.get("/settings", menu_controllers.get_settingsMenu);
router.get("/reports", menu_controllers.get_reportsMenu);

module.exports = router;