<template>
  <v-app dark>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Identifier </span>
        <span class="font-weight-light">for audio and image files</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>

    <v-content>
      <Encode/>
      <Decode/>
    </v-content>
  </v-app>
</template>

<script>
import Encode from './components/Encode'
import Decode from './components/Decode'

export default {
  name: 'App',
  components: {
      Encode,
      Decode
  },
  data () {
    return {
      //
    }
  }
}
</script>
