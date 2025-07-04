import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";

import InfoIcon from "@mui/icons-material/Info";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import ArrowGraph from "./ArrowGraph";
import Graph from "./Graph";
import Table from "./Table";

import {
  ACTIVITY_COMPLETIONS,
  ACTIVITY_COMPLETIONS_PQL,
  ACTIVITY_FREQUENCY,
  ACTIVITY_FREQUENCY_PQL,
  AVERAGE_ACTIVITY_DURATION,
  AVERAGE_CASE_DURATION,
  AVERAGE_WORKLOAD,
  AVERAGE_WORKLOAD_PQL,
  CASE_COMPLETIONS,
  CASE_COMPLETIONS_PQL,
  COMPUTE_DECLARATIVE_CONSTRAINTS,
  COMPUTE_SKELETON,
  DISTINCT_ACTIVITIES,
  DISTINCT_ACTIVITIES_PQL,
  FRACTION_CASE_COMPLETIONS,
  FRACTION_CASE_COMPLETIONS_PQL,
  GET_ABSENCE_VIOLATIONS,
  GET_ACTIVITY_FREQUENCIES,
  GET_ALTPRECEDENCE_VIOLATIONS,
  GET_ALTSUCCESION_VIOLATIONS,
  GET_ALWAYS_AFTER,
  GET_ALWAYS_AFTER_PQL,
  GET_ALWAYS_BEFORE,
  GET_ALWAYS_BEFORE_PQL,
  GET_CHAINPRECEDENCE_VIOLATIONS,
  GET_CHAINRESPONSE_VIOLATIONS,
  GET_CHAINSUCCESION_VIOLATIONS,
  GET_COEXISTENCE_VIOLATIONS,
  GET_DECL_ALWAYS_AFTER_PQL,
  GET_DECL_ALWAYS_BEFORE_PQL,
  GET_DIRECTLY_FOLLOWS,
  GET_DIRECTLY_FOLLOWS_AND_COUNT_PQL,
  GET_EQUIVALENCE,
  GET_EQUIVALENCE_PQL,
  GET_EXACTLY_ONE_VIOLATIONS,
  GET_EXISTANCE_VIOLATIONS,
  GET_GENERAL_INSIGHTS,
  GET_INIT_VIOLATIONS,
  GET_NEVER_TOGETHER,
  GET_NEVER_TOGETHER_PQL,
  GET_NONCHAINSUCCESION_VIOLATIONS,
  GET_NONCOEXISTENCE_VIOLATIONS,
  GET_NONSUCCESION_VIOLATIONS,
  GET_PRECEDENCE_VIOLATIONS,
  GET_RESPONDED_EXISTENCE_VIOLATIONS,
  GET_RESPONSE_VIOLATIONS,
  GET_RESULT_TEMPORAL_PROFILE,
  GET_SUCCESSION_VIOLATIONS,
  GROUP_COVERAGE,
  GROUP_MEMBER_CONTRIBUTION,
  GROUP_RELATIVE_FOCUS,
  GROUP_RELATIVE_STATE,
  HANDOVER_OF_WORK,
  INTERACTION_TWO_RESOURCES,
  INTERACTION_TWO_RESOURCES_PQL,
  MULTITASKING,
  RESOURCE_BASED,
  ROLE_DISCOVERY,
  SIMILAR_ACTIVITIES,
  SOCIAL_POSITION,
  SUBCONTRACTING,
  TEMPORAL_PROFILE,
  WORKING_TOGETHER,
} from "./config";

// -------------------- Log Skeleton Options --------------------

const LOG_SKELETON_OPTIONS = [
  {
    label: "Get Equivalence",
    value: "get_equivalence",
    endpoint: GET_EQUIVALENCE,
  },
  {
    label: "Get Equivalence (PQL)",
    value: "get_equivalence_pql",
    endpoint: GET_EQUIVALENCE_PQL,
  },
  {
    label: "Always Before",
    value: "get_always_before",
    endpoint: GET_ALWAYS_BEFORE,
  },
  {
    label: "Always Before (PQL)",
    value: "get_always_before_pql",
    endpoint: GET_ALWAYS_BEFORE_PQL,
  },
  {
    label: "Always After",
    value: "get_always_after",
    endpoint: GET_ALWAYS_AFTER,
  },
  {
    label: "Always After (PQL)",
    value: "get_always_after_pql",
    endpoint: GET_ALWAYS_AFTER_PQL,
  },
  {
    label: "Never Together",
    value: "get_never_together",
    endpoint: GET_NEVER_TOGETHER,
  },
  {
    label: "Never Together (PQL)",
    value: "get_never_together_pql",
    endpoint: GET_NEVER_TOGETHER_PQL,
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
  {
    label: "Directly Follows and Count (PQL)",
    value: "get_directly_follows_and_count",
    endpoint: GET_DIRECTLY_FOLLOWS_AND_COUNT_PQL,
  },
];

// -------------------- Log Skeleton Descriptions --------------------
const logSkeletonDescriptions = {
  "Get Equivalence":
    "Pairs of activities, where both activities occur equally often in every trace.",
  "Get Equivalence (PQL)":
    "Pairs of activities, where both activities occur equally often in every trace using PQL queries.",
  "Always Before":
    "Pairs of activities, where the first activity always occurs before the second one.",
  "Always Before (PQL)":
    "Pairs of activities, where the first activity always occurs before the second one using PQL queries.",
  "Always After":
    "Pairs of activities, where the second activity always occurs after the first one.",
  "Always After (PQL)":
    "Pairs of activities, where the second activity always occurs after the first one using PQL queries.",
  "Never Together":
    "Pairs of activities that do not occur together in any trace..",
  "Never Together (PQL)":
    "Pairs of activities that do not occur together in any trace using PQL queries.",
  "Directly Follows":
    "Pairs of activities, where the first activity can be followed by the second one.",
  "Activity Frequencies": "Counts how frequently each activity occurs.",
  "Directly Follows and Count (PQL)":
    "Pairs of activities, where the first activity can be followed by the second one. The count of occurrences is also provided using PQL queries.",
};

// --------------------Declarative Constraints Options --------------------
const DECLARATIVE_OPTIONS = [
  { label: "Existence", endpoint: GET_EXISTANCE_VIOLATIONS },
  { label: "Never", endpoint: GET_ABSENCE_VIOLATIONS },
  { label: "Exactly Once", endpoint: GET_EXACTLY_ONE_VIOLATIONS },
  { label: "Initially", endpoint: GET_INIT_VIOLATIONS },
  {
    label: "Responded Existence",
    endpoint: GET_RESPONDED_EXISTENCE_VIOLATIONS,
  },
  {
    label: "Co-Existence",
    endpoint: GET_COEXISTENCE_VIOLATIONS,
  },
  {
    label: "Always After",
    value: "always_after_decl",
    endpoint: GET_RESPONSE_VIOLATIONS,
  },
  {
    label: "Always After (PQL)",
    value: "always_after_pql",
    endpoint: GET_DECL_ALWAYS_AFTER_PQL,
  },
  {
    label: "Always Before",
    value: "always_before_decl",
    endpoint: GET_PRECEDENCE_VIOLATIONS,
  },
  {
    label: "Always Before (PQL)",
    value: "always_before_pql",
    endpoint: GET_DECL_ALWAYS_BEFORE_PQL,
  },
  {
    label: "Succession",
    value: "succession",
    endpoint: GET_SUCCESSION_VIOLATIONS,
  },
  {
    label: "Alternate Precedence",
    value: "alternate_precedence_decl",
    endpoint: GET_ALTPRECEDENCE_VIOLATIONS,
  },
  {
    label: "Alternate Succession",
    value: "alternate_succession_decl",
    endpoint: GET_ALTSUCCESION_VIOLATIONS,
  },
  {
    label: "Immediately After",
    value: "immediately_after_decl",
    endpoint: GET_CHAINRESPONSE_VIOLATIONS,
  },
  {
    label: "Immediately Before",
    value: "immediately_before_decl",
    endpoint: GET_CHAINPRECEDENCE_VIOLATIONS,
  },
  {
    label: "Chain Succession",
    value: "chain_succession_decl",
    endpoint: GET_CHAINSUCCESION_VIOLATIONS,
  },
  {
    label: "Non Co-Existence",
    endpoint: GET_NONCOEXISTENCE_VIOLATIONS,
  },
  {
    label: "Non Succession",
    value: "non_succession",
    endpoint: GET_NONSUCCESION_VIOLATIONS,
  },
  {
    label: "Non Chain Succession",
    value: "non_chain_succession",
    endpoint: GET_NONCHAINSUCCESION_VIOLATIONS,
  },
];

// -------------------- Declarative Constraints Descriptions --------------------
const declarativeDescriptions = {
  Existence:
    "Ensures that a particular activity occurs at least once in each trace.",
  Never: "Specifies that a particular activity must not occur in some traces.",
  "Exactly Once": "Requires that an activity occurs exactly once per trace.",
  Initially:
    "Requires that a specific activity is the first event in every trace.",
  "Responded Existence":
    "If Activity A occurs, then Activity B must also occur somewhere in the trace.",
  "Co-Existence":
    "Activities A and B must either both be present or both be absent in a trace.",
  "Always After":
    "If Activity A occurs, Activity B must follow it at some point in the trace.",
  "Always After (PQL)":
    "If Activity A occurs, Activity B must follow it at some point in the trace using PQL queries.",
  "Always Before":
    "If Activity B occurs, Activity A must have occurred earlier in the same trace.",
  "Always Before (PQL)":
    "If Activity B occurs, Activity A must have occurred earlier in the same trace using PQL queries.",
  Succession:
    "This constraint specifies that if activity A happens, then activity B must happen at some point after A in the same process instance. It allows for other activities to occur between A and B, and it doesn't require B to always follow A.",
  "Alternate Precedence":
    "Every occurrence of Activity B must be preceded by exactly one occurrence of Activity A, with no A in between.",
  "Alternate Succession":
    "Every occurrence of Activity A must be followed by exactly one occurrence of Activity B, with no B in between.",
  "Immediately After":
    "Activity B must directly follow Activity A whenever A occurs.",
  "Immediately Before":
    "Activity A must directly precede Activity B whenever B occurs.",
  "Chain Succession":
    "Every occurrence of Activity A must be immediately followed by B, and every B must be preceded by A.",
  "Non Co-Existence":
    "Activities A and B cannot both appear in the same trace.",
  "Non Succession": "Activity A should never be followed by Activity B.",
  "Non Chain Succession": "Activity B must not immediately follow Activity A.",
};

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
    "Distinct Activities (using PQL)",
    "Activity Frequency",
    "Activity Frequency (using PQL)",
    "Activity Completions",
    "Activity Completions (using PQL)",
    "Case-Completions",
    "Case-Completions (using PQL)",
    "Fraction-Case Completions",
    "Fraction-Case Completions (using PQL)",
    "Average workload",
    "Average workload (using PQL)",
    "Multitasking",
    "Average Activity Duration",
    "Average case duration",
    "Interaction Two Resources",
    "Interaction Two Resources (using PQL)",
    "Social Position",
  ],
  organizational_mining: [
    "Group Relative Focus",
    "Group Relative Stake",
    "Group Coverage",
    "Group Member Contributions",
  ],
};

// -------------------- Resource Descriptions --------------------
const resourceDescriptions = {
  "Handover of Work":
    "The Handover of Work metric measures how many times an individual is followed by another individual in the execution of a business process.",
  Subcontracting:
    "The Subcontracting metric calculates how many times the work of an individual is interleaved by the work of another individual, only to eventually “return” to the original individual.",
  "Working together":
    "The Working Together metric calculates how many times two individuals work together to resolve a process instance.",
  "Similar Activities":
    "The Similar Activities metric calculates how similar the work patterns are between two individuals.",
  "Role Discovery":
    "The organizational role is a set of activities in the log that are executed by a similar (multi)set of resources.",
  "Group Relative Focus":
    "The Group Relative Focus metric specifies for a given work how much a resource group performed this type of work compared to the overall workload of the group. It can be used to measure how the workload of a resource group is distributed over different types of work, i.e., work diversification of the group.",
  "Group Relative Stake":
    "The Group Relative Stake metric specifies for a given work how much this type of work was performed by a certain resource group among all groups. It can be used to measure how the workload devoted to a certain type of work is distributed over resource groups in an organizational model, i.e., work participation by different groups.",
  "Group Coverage":
    "The Group Coverage metric with respect to a given type of work, specifies the proportion of members of a resource group that performed this type of work.",
  "Group Member Contributions":
    "The Group Member Contribution metric of a member of a resource group with respect to a given type of work specifies how much of this type of work by the group was performed by the member. It can be used to measure how the workload of the entire group devoted to a certain type of work is distributed over the group members.",
  "Distinct Activities":
    "Number of distinct activities done by a resource in a given time interval [t1, t2).",
  "Distinct Activities (using PQL)":
    "Number of distinct activities done by a resource in a given time interval [t1, t2) using PQL Queries.",
  "Activity Frequency":
    "Fraction of completions of a given activity a by a given resource r during a given time slot [t1, t2), with respect to the total number of activity completions by resource r during [t1, t2).",
  "Activity Frequency (using PQL)":
    "Fraction of completions of a given activity a by a given resource r during a given time slot [t1, t2), with respect to the total number of activity completions by resource r during [t1, t2) using PQL queries.",
  "Activity Completions":
    "The number of activity instances completed by a given resource during a given time slot.",
  "Activity Completions (using PQL)":
    "The number of activity instances completed by a given resource during a given time slot using PQL queries.",
  "Case-Completions":
    "The number of cases completed during a given time slot in which a given resource was involved.",
  "Case-Completions (using PQL)":
    "The number of cases completed during a given time slot in which a given resource was involved using PQL queries.",
  "Fraction-Case Completions":
    "The fraction of cases completed during a given time slot in which a given resource was involved with respect to the total number of cases completed during the time slot.",
  "Fraction-Case Completions (using PQL)":
    "The fraction of cases completed during a given time slot in which a given resource was involved with respect to the total number of cases completed during the time slot using PQL queries.",
  "Average workload":
    "The average number of activities started by a given resource but not completed at a moment in time.",
  "Average workload (using PQL)":
    "The average number of activities started by a given resource but not completed at a moment in time using PQL queries.",
  Multitasking:
    "The fraction of active time during which a given resource is involved in more than one activity with respect to the resource's active time.",
  "Average Activity Duration":
    "The average duration of instances of a given activity completed during a given time slot by a given resource.",
  "Average case duration":
    "The average duration of cases completed during a given time slot in which a given resource was involved.",
  "Interaction Two Resources":
    "The number of cases completed during a given time slot in which two given resources were involved.",
  "Interaction Two Resources (using PQL)":
    "The number of cases completed during a given time slot in which two given resources were involved using PQL queries.",
  "Social Position":
    "The fraction of resources involved in the same cases with a given resource during a given time slot with respect to the total number of resources active during the time slot.",
};

// -------------------- Main Component --------------------

const ResultsPage = () => {
  const [view, setView] = useState("general"); // Default view

  //general insights
  const [generalInsightsTables, setGeneralInsightsTables] = useState([]);
  const [generalLoading, setGeneralLoading] = useState(false);

  // Shared Output Space
  const [graphData, setGraphData] = useState([]);
  const [tableData, setTableData] = useState([]);

  // Log Skeleton
  const [jobId, setJobId] = useState(null);
  const [selectedOption, setSelectedOption] = useState("");
  const [jobLoading, setJobLoading] = useState(false);

  // Temporal Profile
  const [zeta, setZeta] = useState("");
  const [temporalJobId, setTemporalJobId] = useState(null);
  const [showResultLoading, setShowResultLoading] = useState(false);

  // Declarative Constraints
  const [minSupport, setMinSupport] = useState("");
  const [minConfidence, setMinConfidence] = useState("");
  const [zetaValue, setZetaValue] = useState("");
  const [declJobId, setDeclJobId] = useState(null);
  const [selectedDeclOption, setSelectedDeclOption] = useState("");
  const [declLoading, setDeclLoading] = useState(false);

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

  // -------------------- General Insights: Fetch Data --------------------
  useEffect(() => {
    const fetchGeneralInsights = async () => {
      setGeneralLoading(true);
      try {
        const res = await fetch(GET_GENERAL_INSIGHTS);
        const data = await res.json();
        setGeneralInsightsTables(data.tables || []);
      } catch (err) {
        alert("Failed to fetch general insights: " + err.message);
      } finally {
        setGeneralLoading(false);
      }
    };

    if (view === "general") {
      fetchGeneralInsights();
    }
  }, [view]);

  // -------------------- Log Skeleton: Fetch Job ID on startup--------------------

  useEffect(() => {
    if (view === "log_skeleton") {
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
    }
  }, [view]);

  // -------------------- Resource-Based: Fetch Job ID on start up--------------------

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

  // -------------------- Clear old outputs when view changes for all insights --------------------
  useEffect(() => {
    setGraphData([]);
    setTableData([]);
    setFloatResult(null);
    setSelectedOption("");
    setSelectedResourceOption("");
    setZeta("");
    setSelectedDeclOption("");
    setResourceInputs({
      resource1: "",
      resource2: "",
      activity: "",
      start_time: "",
      end_time: "",
    });
  }, [view]);

  // ------------------------------------ Log Skeleton---------------------------------------------------
  // -------------------- Log Skeleton: Handle Option Selection after we have job id --------------------

  const handleOptionSelect = async (option) => {
    setSelectedOption(option.value);
    setGraphData([]);
    setTableData([]);
    setJobLoading(true);

    // Check if it's a PQL option
    const isPQL = option.label.endsWith("(PQL)");
    const endpoint = option.endpoint;

    try {
      let attempts = 0;
      let resultData = null;

      while (attempts < 20) {
        const res = await fetch(isPQL ? endpoint : `${endpoint}/${jobId}`);
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

  // --------------------------- TEMPORAL PROFILE---------------------------
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

  // --------------------------- DECLARATIVE CONSTRAINTS ---------------------------
  // -------------------- Declarative Constraints: Submit Inputs --------------------

  const handleComputeDeclarative = async () => {
    if (!minSupport || !minConfidence) {
      alert("Please enter both minimum support and minimum confidence.");
      return;
    }

    try {
      const queryParams = new URLSearchParams({
        min_support: parseFloat(minSupport),
        min_confidence: parseFloat(minConfidence),
      });
      if (zetaValue) {
        queryParams.append("fitness_score", parseFloat(zetaValue));
      }
      const url = `${COMPUTE_DECLARATIVE_CONSTRAINTS}?${queryParams.toString()}`;
      const res = await fetch(url, { method: "GET" });
      const data = await res.json();
      setDeclJobId(data.job_id);
      alert(
        "Constraints computation started. Now select a Declarative Insight."
      );
    } catch (err) {
      alert("Error computing declarative constraints: " + err.message);
    }
  };

  const handleDeclarativeOptionSelect = async (option) => {
    const isPQL = option.label.endsWith("(PQL)");
    if (!isPQL && !declJobId) {
      alert("Please compute constraints first.");
      return;
    }

    setSelectedDeclOption(option.value || "");
    setGraphData([]);
    setTableData([]);
    setDeclLoading(true);

    try {
      let attempts = 0;
      let resultData = null;
      const endpoint = option.endpoint;
      const fetchURL = isPQL ? endpoint : `${endpoint}/${declJobId}`;

      while (attempts < 20) {
        const res = await fetch(fetchURL);
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
      alert("Failed to fetch declarative constraint result: " + err.message);
    } finally {
      setDeclLoading(false);
    }
  };

  // ----------------------------------- RESOURCE BASED ---------------------------------------------
  // -------------------- Resource-Based: Handle SNA, Org Mining, Role Discovery --------------------

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

  // -------------------- Resource Based: Handle Input and Submit for Resource Profiles --------------------

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
      case "Distinct Activities (using PQL)":
      case "Activity Completions":
      case "Activity Completions (using PQL)":
      case "Case-Completions":
      case "Case-Completions (using PQL)":
      case "Fraction-Case Completions":
      case "Fraction-Case Completions (using PQL)":
      case "Average workload":
      case "Average workload (using PQL)":
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
      case "Interaction Two Resources (using PQL)":
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
      "Distinct Activities (using PQL)": DISTINCT_ACTIVITIES_PQL,
      "Activity Frequency": ACTIVITY_FREQUENCY,
      "Activity Frequency (using PQL)": ACTIVITY_FREQUENCY_PQL,
      "Activity Completions": ACTIVITY_COMPLETIONS,
      "Activity Completions (using PQL)": ACTIVITY_COMPLETIONS_PQL,
      "Case-Completions": CASE_COMPLETIONS,
      "Case-Completions (using PQL)": CASE_COMPLETIONS_PQL,
      "Fraction-Case Completions": FRACTION_CASE_COMPLETIONS,
      "Fraction-Case Completions (using PQL)": FRACTION_CASE_COMPLETIONS_PQL,
      "Average workload": AVERAGE_WORKLOAD,
      "Average workload (using PQL)": AVERAGE_WORKLOAD_PQL,
      Multitasking: MULTITASKING,
      "Average Activity Duration": AVERAGE_ACTIVITY_DURATION,
      "Average case duration": AVERAGE_CASE_DURATION,
      "Interaction Two Resources": INTERACTION_TWO_RESOURCES,
      "Interaction Two Resources (using PQL)": INTERACTION_TWO_RESOURCES_PQL,
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

  // -------------------- Render Graphs & Tables (Common for all Insights)--------------------

  const renderGraphAndTable = () => (
    <>
      {/* Graphs with arrows for Log Skeleton, Temporal Profile, Declarative Constraints, and Resource-Based Insights  */}
      {graphData.map((graph, idx) => {
        const useArrowGraph = [
          "get_always_before_pql",
          "get_always_after_pql",
          "get_directly_follows_and_count",
          "always_after_decl",
          "always_after_pql",
          "always_before_decl",
          "always_before_pql",
          "succession",
          "alternate_precedence_decl",
          "alternate_succession_decl",
          "immediately_after_decl",
          "immediately_before_decl",
          "chain_succession_decl",
          "non_succession",
          "non_chain_succession",
        ].includes(selectedOption || selectedDeclOption);

        return (
          <Box key={idx} sx={{ mt: 4 }}>
            <Typography variant="h6">Graph {idx + 1}</Typography>
            {useArrowGraph ? (
              <ArrowGraph graphData={graph} />
            ) : (
              <Graph graphData={graph} />
            )}
          </Box>
        );
      })}

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

  // ------------------------- UI Properties------------------------------------

  return (
    <Card sx={{ mx: "auto", mt: 4, maxWidth: 1000, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Results Page
        </Typography>

        {/* -------- View Selector -------- */}
        <Box sx={{ display: "flex", gap: 2, my: 2 }}>
          <Button
            variant={view === "general" ? "contained" : "outlined"}
            onClick={() => setView("general")}
          >
            General Insights
          </Button>
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

        {/* -------- General Insights Section -------- */}
        {view === "general" && (
          <>
            {generalLoading ? (
              <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
                <CircularProgress />
              </Box>
            ) : (
              <>
                {generalInsightsTables.map((table, idx) => (
                  <Box key={idx} sx={{ mt: 4 }}>
                    <Typography variant="h6">Table {idx + 1}</Typography>
                    <Table headers={table.headers} rows={table.rows} />
                  </Box>
                ))}
                {!generalInsightsTables.length && (
                  <Typography color="text.secondary" sx={{ mt: 2 }}>
                    No general insights available.
                  </Typography>
                )}
              </>
            )}
          </>
        )}
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
                renderValue={(value) => {
                  const label =
                    LOG_SKELETON_OPTIONS.find((opt) => opt.value === value)
                      ?.label || value;
                  return (
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                      <span>{label}</span>
                      {logSkeletonDescriptions[label] && (
                        <Tooltip
                          title={
                            <Box
                              sx={{
                                fontSize: 14,
                                lineHeight: 1.6,
                                maxWidth: 300,
                              }}
                            >
                              {logSkeletonDescriptions[label]}
                            </Box>
                          }
                          arrow
                          placement="right"
                        >
                          <IconButton size="small" sx={{ ml: 1 }}>
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      )}
                    </Box>
                  );
                }}
              >
                {LOG_SKELETON_OPTIONS.map((opt) => (
                  <MenuItem key={opt.value} value={opt.value}>
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                      <span>{opt.label}</span>
                      {logSkeletonDescriptions[opt.label] && (
                        <Tooltip
                          title={
                            <Box
                              sx={{
                                fontSize: 14,
                                lineHeight: 1.6,
                                maxWidth: 300,
                              }}
                            >
                              {logSkeletonDescriptions[opt.label]}
                            </Box>
                          }
                          arrow
                          placement="right"
                        >
                          <IconButton size="small" sx={{ ml: 1 }}>
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      )}
                    </Box>
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
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <Button variant="outlined" onClick={handleFetchTemporalResults}>
                Show Temporal Results
              </Button>
              <Tooltip
                title={
                  <Box sx={{ fontSize: 14, lineHeight: 1.6, maxWidth: 300 }}>
                    The temporal conformance results consist of the source
                    activity of the recorded deviation, the target activity of
                    the recorded deviation, the time passed between the
                    occurrence of the source activity and the target activity,
                    and the value of (time passed - mean)/std for this
                    occurrence (zeta).
                  </Box>
                }
                placement="right"
                arrow
              >
                <IconButton size="medium">
                  <InfoIcon fontSize="medium" />
                </IconButton>
              </Tooltip>
            </Box>

            {showResultLoading ? (
              <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
                <CircularProgress />
              </Box>
            ) : (
              renderGraphAndTable()
            )}
          </Box>
        )}

        {/* -------- Declarative Constraints Section -------- */}
        {view === "declarative" && (
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <TextField
              label="Minimum Support Ratio (Range: 0.0 - 1.0) (Best Value: 0.3)"
              variant="outlined"
              type="number"
              value={minSupport}
              onChange={(e) => setMinSupport(e.target.value)}
              fullWidth
            />
            <TextField
              label="Minimum Confidence Ratio (Range: 0.0 - 1.0) (Best Value: 0.7)"
              variant="outlined"
              type="number"
              value={minConfidence}
              onChange={(e) => setMinConfidence(e.target.value)}
              fullWidth
            />
            <TextField
              label="Fitness Score  (Range: 0.0 - 1.0) (Best Value: 1.0)"
              variant="outlined"
              type="number"
              value={zetaValue}
              onChange={(e) => setZetaValue(e.target.value)}
              fullWidth
            />
            <Button variant="contained" onClick={handleComputeDeclarative}>
              Submit Constraints
            </Button>

            {declJobId && (
              <FormControl fullWidth>
                <InputLabel>Declarative Insight</InputLabel>
                <Select
                  value={selectedDeclOption}
                  label="Declarative Insight"
                  onChange={(e) =>
                    handleDeclarativeOptionSelect(
                      DECLARATIVE_OPTIONS.find(
                        (opt) => opt.label === e.target.value
                      )
                    )
                  }
                >
                  {DECLARATIVE_OPTIONS.map((opt) => (
                    <MenuItem key={opt.label} value={opt.label}>
                      <Box sx={{ display: "flex", alignItems: "center" }}>
                        <span>{opt.label}</span>
                        {declarativeDescriptions[opt.label] && (
                          <Tooltip
                            title={
                              <Box
                                sx={{
                                  fontSize: 14,
                                  lineHeight: 1.6,
                                  maxWidth: 300,
                                }}
                              >
                                {declarativeDescriptions[opt.label]}
                              </Box>
                            }
                            arrow
                            placement="right"
                          >
                            <IconButton size="small" sx={{ ml: 1 }}>
                              <InfoIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )}
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}

            {declLoading ? (
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

            {/* -------- Resource Insight Dropdown under Resource Profiles for Resource-Based conformance-------- */}
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
                      <Box sx={{ display: "flex", alignItems: "center" }}>
                        <span>{opt}</span>
                        <Tooltip
                          title={
                            <Box
                              sx={{
                                fontSize: 14,
                                lineHeight: 1.6,
                                maxWidth: 300,
                              }}
                            >
                              {resourceDescriptions[opt] ||
                                "No description available."}
                            </Box>
                          }
                          arrow
                          placement="right"
                        >
                          <IconButton size="small" sx={{ ml: 1 }}>
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}

            {/* -------- Circular Waiting Animation -------- */}
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
