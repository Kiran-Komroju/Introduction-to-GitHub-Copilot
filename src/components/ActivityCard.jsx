import React from 'react';
import './ActivityCard.css';

function ActivityCard({ activity }) {
  return (
    <div className="activity-card">
      <div className="activity-details">
        <h2 className="activity-title">{activity.title}</h2>
        <p className="activity-description">{activity.description}</p>
        <div className="participants-section">
          <h3>Participants</h3>
          <ul>
            {activity.participants && activity.participants.length > 0 ? (
              activity.participants.map((p, idx) => (
                <li key={idx} className="participant-name">{p}</li>
              ))
            ) : (
              <li className="no-participants">No participants yet.</li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ActivityCard;