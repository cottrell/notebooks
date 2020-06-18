<template>
  <v-app>
    <v-app-bar app color="blue" dark >
      <div class="d-flex align-center">
      THIS IS HERE
      </div>

      <v-spacer></v-spacer>

        <span class="mr-2">SOMETHING?</span>
        <v-icon>visibility</v-icon>
    </v-app-bar>

    <v-content>
      <HelloWorld/>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import HelloWorld from './components/HelloWorld.vue';

export default Vue.extend({
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    //
  }),
});
</script>
