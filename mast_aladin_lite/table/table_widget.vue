<template>
  <div v-if="show_if_empty || items.length" style="margin: 20px">
    <v-row style="max-width: 400px;">
      <v-col>
      <div class="row-select">
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
    </v-row>
    <v-row>
    <v-col style="margin-left: 15px">
      <v-row>
        <v-switch v-model="show_tooltips" color="rgb(0, 97, 126)" style="width: 15vw;" label="Show column definition on hover"></v-switch>
      </v-row>
      <v-row>
        <v-label><jupyter-widget :widget="popout_button"></jupyter-widget> Popout widget</v-label>
      </v-row>
    </v-col>
    </v-row>
    <v-row>
      <div class="table-component">
      <v-container>
      <v-data-table
        dense
        :headers="headers_visible_sorted_description"
        :items="items"
        :item-key="item_key"
        :show-select="show_rowselect"
        :single-select="!multiselect"
        :items-per-page="items_per_page"
        v-model="selected_rows"
        class="elevation-2"
      >
      <template v-for="h in headers_visible_sorted_description" v-slot:[`header.${h.value}`]="{ header }">
        <div v-if="show_tooltips" style="color: white;">
          <v-tooltip top>
            <template v-slot:activator="{ on }">              
              <span v-on="on"><strong>{{h.name}}</strong></span>
            </template>
              <p style="width: 300px">
                <strong>{{h.name}}</strong>: {{h.description}}
              </p>
          </v-tooltip>
        </div>
        <div v-else>
            <span><strong>{{h.name}}</strong></span>
        </div>
      </template>
      </v-data-table>
      </v-container>
      </div>
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
    headers_visible_sorted_description() {
      return this.headers_visible_sorted.map(item => {return {'name': item, 'value': item, 'description': this.column_descriptions.find(entry => entry.name == item).description}});
    }
  },
  props: ['column_descriptions', 'show_tooltips'],
};
</script>


<style scoped>
.table-component {
  thead {
      background-color: rgb(0, 97, 126); /* MAST button background lighter-blue color */
    }
}
</style>