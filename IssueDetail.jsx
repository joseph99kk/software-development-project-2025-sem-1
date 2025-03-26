import React from "react";

function IssueDetail ({ issue }) {
    return(
        <div>
            <h3>Issue Details</h3>
            <p>ID: {issue.id}</p>
            <p>Title: {issue.title}</p>
            <p>Description: {issue.description}</p>
            <p>Status: {issue.status}</p>
        </div>
    );
};

export default IssueDetail;