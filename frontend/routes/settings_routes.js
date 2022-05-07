const express                   = require("express");
const settings_controllers       = require("../controllers/settings_controllers");

const router                    = express.Router();

router.get("/systemParameterSetup", settings_controllers.get_setup);
router.get("/defCompWeightsSetup", settings_controllers.get_weights);
router.post("/defCompWeightsSetup", settings_controllers.set_weights);

module.exports = router;