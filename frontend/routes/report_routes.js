const express                   = require("express");
const reports_controllers       = require("../controllers/reports_controllers");

const router                    = express.Router();

router.get("/overview", reports_controllers.get_overview);
router.get("/overview/:ps_id", reports_controllers.get_overview_detail);
router.post("/overview/filter", reports_controllers.filter_employees);
router.get("/careerAspiration", reports_controllers.get_aspiration);
router.post("/careerAspiration/detail", reports_controllers.get_aspiration_employee);
router.get("/careerAspiration/:ps_id", reports_controllers.get_aspiration_detail);
router.post("/careerAspiration/reloadWeights", reports_controllers.get_aspiration_employee);
router.get("/stagnation", reports_controllers.get_stagnation);
router.get("/stagnation/:ps_id", reports_controllers.get_stagnation_detail);

module.exports = router;