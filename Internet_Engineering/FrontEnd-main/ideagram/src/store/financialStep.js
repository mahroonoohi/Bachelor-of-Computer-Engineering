import { createSlice } from "@reduxjs/toolkit";

const financialStepsSlice = createSlice({
  name: "financialStep",
  initialState: { financialSteps: [], financialStepsNum: 0 },
  reducers: {
    addFinancialStep(state, action) {
      const newItem = action.payload;
      const existingItem = state.financialSteps.find(
        (item) => item.uuid === newItem.uuid
      );

      if (!existingItem) {
        state.financialStepsNum++;
        state.financialSteps.push({
          uuid: newItem.uuid,
          step: newItem.step,
          priority: newItem.priority,
          cost: newItem.cost,
          description: newItem.description,
        });
        console.log(state.financialSteps);
      }
    },
    deleteFinancialStep(state, action) {
      const newItem = action.payload;
      const existingItem = state.financialSteps.find(
        (item) => item.uuid === newItem.uuid
      );

      if (existingItem) {
        state.financialStepsNum--;
        state.financialSteps = state.financialSteps.filter(
          (task) => task.uuid !== newItem.uuid
        );
      }
    },
    deleteAll(state, action) {
      state.financialSteps = [];
      state.financialStepsNum = 0;
    },
  },
});

export const financialStepsActions = financialStepsSlice.actions;

export const financialStepsReducer = financialStepsSlice.reducer;
