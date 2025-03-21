<template>

  <div class="table-component" v-if="show_if_empty || items.length">
    <v-row>
      <v-col>
      <div class="row-select" style="margin-bottom: -20px;">
        <v-select
          class="no-hint"
          v-model="headers_visible"
          :items="headers_avail"
          @change="$emit('update:headers_visible', $event)"
          label="Display columns"
          multiple
          dense
        >
        <template v-slot:selection="{ item, index }">
          <span
            v-if="index === 0"
            class="grey--text text-caption"
          >
            ({{ headers_visible.length}} selected)
          </span>
        </template>
        <template v-slot:prepend-item>
          <v-list-item
            ripple
            @mousedown.prevent
            @click="() => {if (headers_visible.length < headers_avail.length) { headers_visible = headers_avail} else {headers_visible = []}}"
          >
            <v-list-item-action>
              <v-icon>
                {{ headers_visible.length == headers_avail.length ? 'mdi-close-box' : headers_visible.length ? 'mdi-minus-box' : 'mdi-checkbox-blank-outline' }}
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>
                {{ headers_visible.length < headers_avail.length ? "Select All" : "Clear All" }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider class="mt-2"></v-divider>
        </template>
        </v-select>
      </div>
      </v-col>
      <v-col>
          <v-row>
              <jupyter-widget :widget="popout_button"></jupyter-widget>
          </v-row>
      </v-col>
    </v-row>
    <v-row style="margin: 5px;">
      <v-data-table
        dense
        :headers="headers_visible_sorted.map(item => {return {'text': item, 'value': item}})"
        :items="items"
        :item-key="item_key"
        :show-select="show_rowselect"
        :single-select="!multiselect"
        :items-per-page="items_per_page"
        v-model="selected_rows"
        class="elevation-2"
      ></v-data-table>
    </v-row>
  </div>
</template>

<script>
module.exports = {
  props: ['popout_button'],
  computed: {
    headers_visible_sorted() {
      return this.headers_avail.filter(item => this.headers_visible.indexOf(item) !== -1);
    },
  }
};
</script>


<style scoped>
  thead {
      background-color: rgb(0, 97, 126); /* MAST button background lighter-blue color */
    }
  .v-data-table-header span {
    color: white  !important;
  }
  tr:hover {
    background-color: #a75000; /* MAST accent color */
  }
</style>