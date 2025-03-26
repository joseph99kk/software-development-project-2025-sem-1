import React from "react";

function IssueList({ issues, selectIssue }) {
    return (
        <div>
            <h3>Issue List</h3>
            <ul>
                {issues.map((issue) => (
                    <li key={issue.id} onClick={() => selectIssue(issue)}>
                        {issue.title}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default IssueList;