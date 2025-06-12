import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Divider,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  CircularProgress,
  TextField,
} from "@mui/material";

import Graph from "./Graph";
import Table from "./Table";

import {
  COMPUTE_SKELETON,
  GET_EQUVALENCE,
  GET_ALWAYS_BEFORE,
  GET_ALWAYS_AFTER,
  GET_NEVER_TOGETHER,
  GET_DIRECTLY_FOLLOWS,
  GET_ACTIVITY_FREQUENCIES,
  GET_RESULT_TEMPORAL_PROFILE,
  TEMPORAL_PROFILE,
  RESOURCE_BASED,
  HANDOVER_OF_WORK,
  SUBCONTRACTING,
  WORKING_TOGETHER,
  SIMILAR_ACTIVITIES,
  GROUP_RELATIVE_FOCUS,
  GROUP_RELATIVE_STATE,
  GROUP_COVERAGE,
  GROUP_MEMBER_CONTRIBUTION,
  ROLE_DISCOVERY,
  DISTINCT_ACTIVITIES,
  ACTIVITY_FREQUENCY,
  ACTIVITY_COMPLETIONS,
  CASE_COMPLETIONS,
  FRACTION_CASE_COMPLETIONS,
  AVERAGE_WORKLOAD,
  MULTITASKING,
  AVERAGE_ACTIVITY_DURATION,
  AVERAGE_CASE_DURATION,
  INTERACTION_TWO_RESOURCES,
  SOCIAL_POSITION,
} from "./config";

// -------------------- Log Skeleton Options --------------------

const LOG_SKELETON_OPTIONS = [
  {
    label: "Get Equivalence",
    value: "get_equivalence",
    endpoint: GET_EQUVALENCE,
  },
  {
    label: "Always Before",
    value: "get_always_before",
    endpoint: GET_ALWAYS_BEFORE,
  },
  {
    label: "Always After",
    value: "get_always_after",
    endpoint: GET_ALWAYS_AFTER,
  },
  {
    label: "Never Together",
    value: "get_never_together",
    endpoint: GET_NEVER_TOGETHER,
  },
  {
    label: "Directly Follows",
    value: "get_directly_follows",
    endpoint: GET_DIRECTLY_FOLLOWS,
  },
  {
    label: "Activity Frequencies",
    value: "get_activity_frequencies",
    endpoint: GET_ACTIVITY_FREQUENCIES,
  },
];

// -------------------- Resource Options --------------------

const resourceOptions = {
  sna: [
    "Handover of Work",
    "Subcontracting",
    "Working together",
    "Similar Activities",
  ],
  role_discovery: ["Role Discovery"],
  resource_profiles: [
    "Distinct Activities",
    "Activity Frequency",
    "Activity Completions",
    "Case-Completions",
    "Fraction-Case Completions",
    "Average workload",
    "Multitasking",
    "Average Activity Duration",
    "Average case duration",
    "Interaction Two Resources",
    "Social Position",
  ],
  organizational_mining: [
    "Group Relative Focus",
    "Group Relative Stake",
    "Group Coverage",
    "Group Member Contributions",
  ],
};

// -------------------- Main Component --------------------

const ResultsPage = () => {
  const [view, setView] = useState("log_skeleton");

  // Shared
  const [graphData, setGraphData] = useState([]);
  const [tableData, setTableData] = useState([]);
  // const [loading, setLoading] = useState(false);

  // Log Skeleton
  const [jobId, setJobId] = useState(null);
  const [selectedOption, setSelectedOption] = useState("");
  const [jobLoading, setJobLoading] = useState(false);

  // Temporal Profile
  const [zeta, setZeta] = useState("");
  const [temporalJobId, setTemporalJobId] = useState(null);
  const [showResultLoading, setShowResultLoading] = useState(false);

  // Resource-based
  const [resourceJobId, setResourceJobId] = useState(null);
  const [selectedResourceType, setSelectedResourceType] = useState("");
  const [selectedResourceOption, setSelectedResourceOption] = useState("");
  const [resourceLoading, setResourceLoading] = useState(false);
  const [floatResult, setFloatResult] = useState(null);

  // Inputs for Resource Profiles
  const [resourceInputs, setResourceInputs] = useState({
    resource1: "",
    resource2: "",
    activity: "",
    start_time: "",
    end_time: "",
  });

  // -------------------- Log Skeleton: Fetch Job ID --------------------

  useEffect(() => {
    const computeJob = async () => {
      try {
        const res = await fetch(COMPUTE_SKELETON, { method: "POST" });
        const data = await res.json();
        setJobId(data.job_id);
      } catch (err) {
        alert("Error starting log skeleton computation: " + err.message);
      }
    };
    computeJob();
  }, []);

  // -------------------- Resource-Based: Fetch Job ID --------------------

  useEffect(() => {
    if (view === "resource") {
      const computeJob = async () => {
        try {
          const res = await fetch(RESOURCE_BASED, { method: "POST" });
          const data = await res.json();
          setResourceJobId(data.job_id);
        } catch (err) {
          alert("Error starting resource-based computation: " + err.message);
        }
      };
      computeJob();
    }
  }, [view]);

  // -------------------- Log Skeleton: Handle Option Selection --------------------

  const handleOptionSelect = async (option) => {
    setSelectedOption(option.value);
    setGraphData([]);
    setTableData([]);
    setJobLoading(true);

    //polling mechanism implementation
    try {
      let attempts = 0;
      let resultData = null;
      while (attempts < 20) {
        const res = await fetch(`${option.endpoint}/${jobId}`);
        if (res.ok) {
          resultData = await res.json();
          break;
        }
        await new Promise((res) => setTimeout(res, 500));
        attempts++;
      }
      if (!resultData) {
        throw new Error("Timeout: backend did not return results in time.");
      }
      setGraphData(resultData.graphs || []);
      setTableData(resultData.tables || []);
    } catch (err) {
      alert("Failed to fetch result: " + err.message);
    } finally {
      setJobLoading(false);
    }
  };

  // -------------------- Temporal Profile: Submit Zeta --------------------

  const handleComputeTemporal = async () => {
    if (!zeta) {
      alert("Please enter a zeta value.");
      return;
    }

    try {
      const res = await fetch(`${TEMPORAL_PROFILE}?zeta=${parseFloat(zeta)}`, {
        method: "POST",
      });
      const data = await res.json();
      setTemporalJobId(data.job_id);
      alert("Zeta submitted successfully. Now click 'Show Temporal Results'.");
    } catch (err) {
      alert("Error computing temporal result: " + err.message);
    }
  };

  // -------------------- Temporal Profile: Fetch Results --------------------

  const handleFetchTemporalResults = async () => {
    if (!temporalJobId) {
      alert("Please submit Zeta first.");
      return;
    }

    setGraphData([]);
    setTableData([]);
    setShowResultLoading(true);

    //polling mechanism implementation
    try {
      let attempts = 0;
      let resultData = null;
      while (attempts < 20) {
        const res = await fetch(
          `${GET_RESULT_TEMPORAL_PROFILE}/${temporalJobId}`
        );
        if (res.ok) {
          resultData = await res.json();
          break;
        }
        await new Promise((res) => setTimeout(res, 500));
        attempts++;
      }
      if (!resultData) {
        throw new Error("Timeout: backend did not return results in time.");
      }
      setGraphData(resultData.graphs || []);
      setTableData(resultData.tables || []);
    } catch (err) {
      alert("Error fetching result: " + err.message);
    } finally {
      setShowResultLoading(false);
    }
  };

  // -------------------- Resource-Based: Handle SNA, Org, Role Discovery --------------------

  const handleSNAOrOrgOption = async (selected) => {
    const endpointMap = {
      "Handover of Work": HANDOVER_OF_WORK,
      Subcontracting: SUBCONTRACTING,
      "Working together": WORKING_TOGETHER,
      "Similar Activities": SIMILAR_ACTIVITIES,
      "Role Discovery": ROLE_DISCOVERY,
      "Group Relative Focus": GROUP_RELATIVE_FOCUS,
      "Group Relative Stake": GROUP_RELATIVE_STATE,
      "Group Coverage": GROUP_COVERAGE,
      "Group Member Contributions": GROUP_MEMBER_CONTRIBUTION,
    };

    const endpoint = endpointMap[selected];
    if (!endpoint || !resourceJobId) return;

    setGraphData([]);
    setTableData([]);
    setResourceLoading(true);

    //polling mechanism implementation
    try {
      let attempts = 0;
      let resultData = null;
      while (attempts < 20) {
        const res = await fetch(`${endpoint}/${resourceJobId}`);
        if (res.ok) {
          resultData = await res.json();
          break;
        }
        await new Promise((res) => setTimeout(res, 500));
        attempts++;
      }
      if (!resultData) {
        throw new Error("Timeout: backend did not return results in time.");
      }
      setGraphData(resultData.graphs || []);
      setTableData(resultData.tables || []);
    } catch (err) {
      alert("Error fetching resource-based result: " + err.message);
    } finally {
      setResourceLoading(false);
    }
  };

  // -------------------- Resource Profiles: Handle Input and Submit --------------------

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setResourceInputs((prev) => ({ ...prev, [name]: value }));
  };

  const submitResourceProfiles = () => {
    alert("Inputs submitted. Now select a resource insight.");
  };

  const handleResourceProfileFetch = async (option) => {
    const queryParams = new URLSearchParams();
    const { resource1, resource2, activity, start_time, end_time } =
      resourceInputs;

    switch (option) {
      case "Distinct Activities":
      case "Activity Completions":
      case "Case-Completions":
      case "Fraction-Case Completions":
      case "Average workload":
      case "Multitasking":
      case "Average case duration":
      case "Social Position":
        queryParams.append("resource", resource1);
        queryParams.append("start_time", start_time);
        queryParams.append("end_time", end_time);
        break;

      case "Activity Frequency":
      case "Average Activity Duration":
        queryParams.append("resource", resource1);
        queryParams.append("activity", activity);
        queryParams.append("start_time", start_time);
        queryParams.append("end_time", end_time);
        break;

      case "Interaction Two Resources":
        queryParams.append("resource1", resource1);
        queryParams.append("resource2", resource2);
        queryParams.append("start_time", start_time);
        queryParams.append("end_time", end_time);
        break;

      default:
        return;
    }

    const endpointMap = {
      "Distinct Activities": DISTINCT_ACTIVITIES,
      "Activity Frequency": ACTIVITY_FREQUENCY,
      "Activity Completions": ACTIVITY_COMPLETIONS,
      "Case-Completions": CASE_COMPLETIONS,
      "Fraction-Case Completions": FRACTION_CASE_COMPLETIONS,
      "Average workload": AVERAGE_WORKLOAD,
      Multitasking: MULTITASKING,
      "Average Activity Duration": AVERAGE_ACTIVITY_DURATION,
      "Average case duration": AVERAGE_CASE_DURATION,
      "Interaction Two Resources": INTERACTION_TWO_RESOURCES,
      "Social Position": SOCIAL_POSITION,
    };

    const url = `${endpointMap[option]}?${queryParams.toString()}`;
    setResourceLoading(true);
    try {
      const res = await fetch(url);
      const text = await res.text();
      const floatVal = parseFloat(text);

      if (!isNaN(floatVal)) {
        setFloatResult(`Output: ${floatVal}`);
      } else {
        alert("Unexpected response format: Not a number.");
        setFloatResult(null);
      }
    } catch (err) {
      alert("Error fetching float metric: " + err.message);
      setFloatResult(null);
    } finally {
      setResourceLoading(false);
    }
  };

  // -------------------- Render Graphs & Tables --------------------

  const renderGraphAndTable = () => (
    <>
      {graphData.map((graph, idx) => (
        <Box key={idx} sx={{ mt: 4 }}>
          <Typography variant="h6">Graph {idx + 1}</Typography>
          <Graph graphData={graph} />
        </Box>
      ))}
      {tableData.map((table, idx) => (
        <Box key={idx} sx={{ mt: 4 }}>
          <Typography variant="h6">Table {idx + 1}</Typography>
          <Table headers={table.headers} rows={table.rows} />
        </Box>
      ))}
      {floatResult !== null && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6">Result</Typography>
          <Typography variant="body1"> 
            {selectedResourceOption
              ? `${selectedResourceOption}: ${floatResult.replace(
                  "Output: ",
                  ""
                )}`
              : floatResult}
          </Typography>
        </Box>
      )}
      {!graphData.length && !tableData.length && floatResult === null && (
        <Typography color="text.secondary" sx={{ mt: 2 }}>
          No data to display.
        </Typography>
      )}
    </>
  );
  // -------------------- UI --------------------

  return (
    <Card sx={{ mx: "auto", mt: 4, maxWidth: 1000, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Conformance Insights
        </Typography>

        {/* -------- View Selector -------- */}
        <Box sx={{ display: "flex", gap: 2, my: 2 }}>
          <Button
            variant={view === "log_skeleton" ? "contained" : "outlined"}
            onClick={() => setView("log_skeleton")}
          >
            Log Skeleton
          </Button>
          <Button
            variant={view === "temporal" ? "contained" : "outlined"}
            onClick={() => setView("temporal")}
          >
            Temporal
          </Button>
          <Button
            variant={view === "declarative" ? "contained" : "outlined"}
            onClick={() => setView("declarative")}
          >
            Declarative
          </Button>
          <Button
            variant={view === "resource" ? "contained" : "outlined"}
            onClick={() => setView("resource")}
          >
            Resource
          </Button>
        </Box>

        <Divider />

        {/* -------- Log Skeleton Section -------- */}
        {view === "log_skeleton" && (
          <>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Select Log Skeleton Operation</InputLabel>
              <Select
                value={selectedOption}
                label="Select Log Skeleton Operation"
                onChange={(e) =>
                  handleOptionSelect(
                    LOG_SKELETON_OPTIONS.find(
                      (opt) => opt.value === e.target.value
                    )
                  )
                }
                disabled={!jobId}
              >
                {LOG_SKELETON_OPTIONS.map((opt) => (
                  <MenuItem key={opt.value} value={opt.value}>
                    {opt.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {jobLoading ? (
              <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
                <CircularProgress />
              </Box>
            ) : (
              renderGraphAndTable()
            )}
          </>
        )}

        {/* -------- Temporal Profile Section -------- */}
        {view === "temporal" && (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <TextField
              label="Zeta Value"
              variant="outlined"
              type="number"
              value={zeta}
              onChange={(e) => setZeta(e.target.value)}
              fullWidth
            />
            <Button variant="contained" onClick={handleComputeTemporal}>
              Submit Zeta
            </Button>
            <Button variant="outlined" onClick={handleFetchTemporalResults}>
              Show Temporal Results
            </Button>

            {showResultLoading ? (
              <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
                <CircularProgress />
              </Box>
            ) : (
              renderGraphAndTable()
            )}
          </Box>
        )}

        {/* -------- Resource-Based Section -------- */}
        {view === "resource" && (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            {/* -------- Resource Perspective Dropdown -------- */}
            <FormControl fullWidth>
              <InputLabel>Resource Perspective</InputLabel>
              <Select
                value={selectedResourceType}
                label="Resource Perspective"
                onChange={(e) => {
                  setSelectedResourceType(e.target.value);
                  setSelectedResourceOption("");
                  setFloatResult(null);
                  setGraphData([]);
                  setTableData([]);
                }}
              >
                <MenuItem value="sna">Social Network Analysis</MenuItem>
                <MenuItem value="role_discovery">Role Discovery</MenuItem>
                <MenuItem value="resource_profiles">Resource Profiles</MenuItem>
                <MenuItem value="organizational_mining">
                  Organizational Mining
                </MenuItem>
              </Select>
            </FormControl>

            {/* -------- Resource Profiles Input Fields -------- */}
            {selectedResourceType === "resource_profiles" && (
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  gap: 2,
                  width: "70%",
                  mt: 2,
                  mx: "auto",
                }}
              >
                <Typography variant="subtitle1" sx={{ fontWeight: "bold" }}>
                  Enter Inputs for Resource Profile
                </Typography>
                <TextField
                  label="Resource 1"
                  name="resource1"
                  value={resourceInputs.resource1}
                  onChange={handleInputChange}
                  fullWidth
                />
                <TextField
                  label="Resource 2 (For interaction between 2 resources)"
                  name="resource2"
                  value={resourceInputs.resource2}
                  onChange={handleInputChange}
                  fullWidth
                />
                <TextField
                  label="Activity"
                  name="activity"
                  value={resourceInputs.activity}
                  onChange={handleInputChange}
                  fullWidth
                />
                <TextField
                  label="Start Time"
                  name="start_time"
                  value={resourceInputs.start_time}
                  onChange={handleInputChange}
                  fullWidth
                />
                <TextField
                  label="End Time"
                  name="end_time"
                  value={resourceInputs.end_time}
                  onChange={handleInputChange}
                  fullWidth
                />
                <Button
                  variant="contained"
                  onClick={submitResourceProfiles}
                  sx={{ width: "fit-content" }}
                >
                  Submit Resource Inputs
                </Button>
              </Box>
            )}

            {/* -------- Resource Insight Dropdown -------- */}
            {selectedResourceType && (
              <FormControl fullWidth>
                <InputLabel>Resource Insight</InputLabel>
                <Select
                  value={selectedResourceOption}
                  label="Resource Insight"
                  onChange={(e) => {
                    const selected = e.target.value;
                    setSelectedResourceOption(selected);

                    if (selectedResourceType === "resource_profiles") {
                      handleResourceProfileFetch(selected);
                    } else {
                      handleSNAOrOrgOption(selected);
                    }
                  }}
                >
                  {resourceOptions[selectedResourceType].map((opt) => (
                    <MenuItem key={opt} value={opt}>
                      {opt}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}

            {/* -------- Results Loading or Output -------- */}
            {resourceLoading ? (
              <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
                <CircularProgress />
              </Box>
            ) : (
              renderGraphAndTable()
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ResultsPage;
