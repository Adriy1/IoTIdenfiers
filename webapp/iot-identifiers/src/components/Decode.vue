<template>
    <v-container>
        <v-card>
            <v-container>
            <v-card-title>
                <span class="headline">Decode File</span>
            </v-card-title>
            <input @change="getfile" id="input_file" type="file" />
                <v-btn @click="submitFile()">
                    submit
                </v-btn>
                <span>{{identifier}}</span>
            </v-container>
        </v-card>
    </v-container>
</template>

<script>
    /* eslint-disable no-console */

    import axios from 'axios';

    export default {
        name: "Decode.vue",
        data: () => ({
            filepath: '',
            identifier: '',
        }),
        methods: {
            getfile (event) {
                // eslint-disable-next-line no-console
                console.log(event.target.files[0]);
                this.filepath = event.target.files[0];
            },
            submitFile(){
                /*
                        Initialize the form data
                    */
                let formData = new FormData();

                /*
                    Add the form data we need to submit
                */
                formData.append('file', this.filepath);
// eslint-disable-next-line no-unused-vars
                var _this = this;
                axios.post( 'http://localhost:5000/decode', formData,)
                    .then((response) => {
                        console.log(response.data);
                        _this.identifier = response.data;
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        }
    }


</script>

<style scoped>

</style>