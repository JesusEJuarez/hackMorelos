const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { MongoClient, ServerApiVersion } = require('mongodb');

const app = express();
const port = 3001;

const uri = "mongodb+srv://leo:123@cluster0.hnpunss.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));  // Servir archivos estáticos desde la carpeta "public"

async function run() {
    try {
        await client.connect();
        const db = client.db('Data_HackMorelos');

        app.post('/agregarMedico', async (req, res) => {
            const { nombre, numero, cedula, correo } = req.body;
            const collection = db.collection('Medicos');
            const document = { nombre, numero, cedula, correo };
            await collection.insertOne(document);
            res.send(`Medico agregado: ${JSON.stringify(document)}`);
        });

        app.post('/agregarPaciente', async (req, res) => {
            const { nombre, edad, numero, medicamentos, horario, cedula, fechaCitaSig, nombreFamiliar, numeroFamiliar } = req.body;
            const collection = db.collection('Pacientes');
            const document = { nombre, edad, numero, medicamentos, horario, cedula, fecha_cita: new Date().toLocaleDateString(), fecha_cita_sig: fechaCitaSig };
            if (nombreFamiliar) document.nombre_familiar = nombreFamiliar;
            if (numeroFamiliar) document.numero_familiar = numeroFamiliar;
            await collection.insertOne(document);
            res.send(`Paciente agregado: ${JSON.stringify(document)}`);
        });

        app.get('/listarPacientes', async (req, res) => {
            const { nombre } = req.query;
            const collection = db.collection('Pacientes');
            const resultados = await collection.find({ nombre }).toArray();
            res.send(resultados);
        });

        app.get('/obtenerCedula', async (req, res) => {
            const { correo } = req.query;
            const collection = db.collection('Medicos');
            const resultados = await collection.find({ correo }).toArray();
            res.send(resultados);
        });

        app.listen(port, () => {
            console.log(`Servidor corriendo en http://localhost:${port}`);
        });
    } catch (e) {
        console.error(e);
    }
}

run().catch(console.dir);
