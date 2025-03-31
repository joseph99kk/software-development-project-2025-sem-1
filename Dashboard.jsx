import React from "react";
import IssueList from "./IssueList";
import Notification from "./Notification";

function Dashboard  ({ issues, selectIssue, notification }) {
  return (
    <div>
      {/* <h2>Student Dashboard</h2> */}
      {/* Rendering a Notification if there's a message */}
      {notification && <Notification message={notification} />}
      {/* Pass issues and selectIssue as props */}
      {/* <IssueList issues={issues} selectIssue={selectIssue} /> */}
    </div>
  );
};

export default Dashboard;
