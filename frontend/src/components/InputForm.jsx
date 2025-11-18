import React, { useState } from 'react';
import './InputForm.css';

function InputForm({ onSubmit, loading, features }) {
  const [formData, setFormData] = useState({
    Age: 35,
    income: 50,
    spending: 50,
    gender: 1
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (checked ? 1 : 0) : parseFloat(value)
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="input-form">
      <div className="form-group">
        <label htmlFor="Age">
          Age: <span className="value">{formData.Age}</span>
        </label>
        <input
          type="range"
          id="Age"
          name="Age"
          min="18"
          max="70"
          value={formData.Age}
          onChange={handleChange}
          className="slider"
        />
        <div className="range-labels">
          <span>18</span>
          <span>70</span>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="income">
          Annual Income (k$): <span className="value">{formData.income}</span>
        </label>
        <input
          type="range"
          id="income"
          name="income"
          min="15"
          max="137"
          value={formData.income}
          onChange={handleChange}
          className="slider"
        />
        <div className="range-labels">
          <span>$15k</span>
          <span>$137k</span>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="spending">
          Spending Score: <span className="value">{formData.spending}</span>
        </label>
        <input
          type="range"
          id="spending"
          name="spending"
          min="1"
          max="100"
          value={formData.spending}
          onChange={handleChange}
          className="slider"
        />
        <div className="range-labels">
          <span>Low</span>
          <span>High</span>
        </div>
      </div>

      <div className="form-group checkbox-group">
        <label htmlFor="gender" className="checkbox-label">
          <input
            type="checkbox"
            id="gender"
            name="gender"
            checked={formData.gender === 1}
            onChange={handleChange}
          />
          <span>Male</span>
        </label>
      </div>

      <button 
        type="submit" 
        disabled={loading}
        className="submit-button"
      >
        {loading ? '⏳ Predicting...' : '🔮 Predict Cluster'}
      </button>
    </form>
  );
}

export default InputForm;
