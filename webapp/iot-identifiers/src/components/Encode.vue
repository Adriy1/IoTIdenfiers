<template>
    <v-container>
        <v-card>
            <v-container>
            <v-card-title>
                <span class="headline">Upload File</span>
            </v-card-title>
            <input @change="getfile" id="input_file" type="file" />
            <v-form>
                <v-text-field
                        v-model="identifier"
                        label="Identifier"
                        required
                ></v-text-field>
                <v-text-field
                        v-model="outputFileName"
                        label="Output file name"
                        required
                ></v-text-field>
                <v-btn @click="submitFile()">
                    submit
                </v-btn>
            </v-form>
                </v-container>
        </v-card>
    </v-container>
</template>

<script>
    /* eslint-disable no-console */

    import axios from 'axios';

    export default {
        data: () => ({
            filepath: '',
            identifier: '',
            outputFileName: ''
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
                formData.append('id', this.identifier);
                formData.append('filename', this.outputFileName);
                var _this = this;
                axios.post( 'http://localhost:5000/upload', formData,{
                    responseType: 'blob'
                })
                    .then((response) => {
                        const url = window.URL.createObjectURL(new Blob([response.data]));
                        const link = document.createElement('a');
                        link.href = url;
                        link.setAttribute('download', _this.outputFileName);
                        document.body.appendChild(link);
                        link.click();
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        }
    }
</script>

<style>

</style>
