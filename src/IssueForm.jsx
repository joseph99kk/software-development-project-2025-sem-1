import React from 'react';

const IssueForm = () => {
  return (
    <div>
      <h2>Submit an Issue</h2>
      <form>
        <input type="text" placeholder="Issue Title" /><br />
        <textarea placeholder="Describe the issue..." /><br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default IssueForm;
