import React from 'react';
import './Visualizer.css';

const Visualizer = ({ active }) => {
    return (
        <div className={`arc-reactor-container ${active ? 'active' : ''}`}>
            <div className="reactor-core-outer">
                <div className="ring ring-1"></div>
                <div className="ring ring-2"></div>
                <div className="ring ring-3"></div>
                <div className="core-glow"></div>
                <div className="data-pulses">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>
    );
};

export default React.memo(Visualizer);
