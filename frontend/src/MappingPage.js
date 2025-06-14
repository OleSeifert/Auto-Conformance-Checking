import React, { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  FormHelperText,
  CircularProgress,
} from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import { COMMIT_LOG_TO_CELONIS } from "./config";

const MappingPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const columns = location.state?.columns || [];

  const [caseIdCol, setCaseIdCol] = useState("");
  const [activityCol, setActivityCol] = useState("");
  const [timestampCol, setTimestampCol] = useState("");
  const [resourceCol1, setResourceCol1] = useState("");
  const [groupCol, setGroupCol] = useState("");

  const [loading, setLoading] = useState(false);

  const selectedValues = [
    caseIdCol,
    activityCol,
    timestampCol,
    resourceCol1,
    groupCol,
  ];

  const getFilteredOptions = (currentValue) =>
    columns.filter(
      (col) => col === currentValue || !selectedValues.includes(col)
    );

  const handleSubmit = async () => {
    const payload = {
      case_id_column: caseIdCol,
      activity_column: activityCol,
      timestamp_column: timestampCol,
      resource_1_column: resourceCol1,
      group_column: groupCol,
    };

    try {
      setLoading(true);
      const res = await fetch(COMMIT_LOG_TO_CELONIS, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await res.json();
      setLoading(false);

      if (result.message === "Table created successfully") {
        alert(result.message);
        navigate("/results", { state: result });
      } else {
        alert("Unexpected response from server.");
      }
    } catch (err) {
      setLoading(false);
      alert("Failed to commit logs: " + err.message);
    }
  };

  const renderDropdown = (label, value, setter, required = true) => (
    <FormControl fullWidth required={required} error={required && !value}>
      <InputLabel>{label}</InputLabel>
      <Select
        value={value}
        onChange={(e) => setter(e.target.value)}
        label={label}
      >
        {getFilteredOptions(value).map((col, i) => (
          <MenuItem key={i} value={col}>
            {col}
          </MenuItem>
        ))}
      </Select>
      {required && !value && <FormHelperText>Required</FormHelperText>}
    </FormControl>
  );

  return (
    <Card sx={{ maxWidth: 600, mx: "auto", mt: 4, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5">Map Columns</Typography>
        <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 2 }}>
          {renderDropdown("Case ID Column", caseIdCol, setCaseIdCol)}
          {renderDropdown("Activity Column", activityCol, setActivityCol)}
          {renderDropdown("Timestamp Column", timestampCol, setTimestampCol)}
          {renderDropdown(
            "Resource Column (optional)",
            resourceCol1,
            setResourceCol1,
            false
          )}
          {renderDropdown(
            "Group Column (optional)",
            groupCol,
            setGroupCol,
            false
          )}

          {loading ? (
            <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
              <CircularProgress />
            </Box>
          ) : (
            <Button variant="contained" onClick={handleSubmit}>
              Confirm Mapping
            </Button>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default MappingPage;
