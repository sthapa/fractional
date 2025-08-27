<script setup>
import { onMounted, ref } from 'vue'
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community';
0
// Register all Community features
ModuleRegistry.registerModules([AllCommunityModule]);

import { AgGridVue } from "ag-grid-vue3"; // Vue Data Grid Component

const API_URL_LIST = `http://localhost:8000/players`
const API_URL_UPDATE = `http://localhost:8000/player/`

const rowData = ref([]);

onMounted(async () => {
    rowData.value = await fetchData();
});


const fetchData = async () => {
    const response = await fetch(API_URL_LIST);
    return response.json();
};

// Column Definitions: Defines the columns to be displayed.
const colDefs = ref([
    { field: "name", filter: true,  editable: true },
    { field: "position", filter: true, editable: true },
    { field: "games" },
    { field: "at_bats" },
    { field: "runs" },
    { field: "hits" },
    { field: "doubles" },
    { field: "triples" },
    { field: "home_runs" },
    { field: "rbi" },
    { field: "walks" },
    { field: "strikeouts" },
    { field: "stolen_bases" },
    { field: "caught_stealing" },
    { field: "avg" },
    { field: "obp" },
    { field: "slugging" },
    { field: "ops" },
    { field: "desc" },
]);

const updatePlayer = async (player) => {
  const request = new Request(`${API_URL_UPDATE}${player.id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(player),
  })
  const response = await fetch(request)
};

function onCellValueChanged(event) {
  let row = event.rowIndex
  console.log(`New Cell Value: ${event.value} ${row}`);
  let rowVal = rowData.value[row];
  updatePlayer(rowVal);
  console.log(`row: ${JSON.stringify(rowVal)}`);
}

</script>

<template>
  <header>

  </header>

  <main>
    <h1>Baseball Stats</h1>
    <ag-grid-vue
        :rowData="rowData"
        :columnDefs="colDefs"
        style="height: 500px; width: 800px;"
        @cell-value-changed="onCellValueChanged">
    </ag-grid-vue>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}


@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }


  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
