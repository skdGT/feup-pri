const express = require('express');
const router = express.Router();
const axios = require('axios');

const TMDB_API_KEY = process.env.TMDB_API_KEY;
const TMDB_URL = 'https://api.themoviedb.org/3/';
const TMDB_IMAGE_URL = 'https://image.tmdb.org/t/p/w500/';

router.get('/poster/:id', (req, res) => {
    const id = req.params.id;

    axios.get(TMDB_URL + 'find/' + id, {
        params: {
            api_key: TMDB_API_KEY,
            external_source: 'imdb_id'
        }
    }).then(results => {
        let movies = results.data.movie_results;
        if (movies.length === 0) {
            res.send({message: 'ERR_NO_MOVIES'});
            return;
        }

        const poster = TMDB_IMAGE_URL + results.data.movie_results[0].poster_path;

        res.send({
            message: {
                poster: poster,
                movie: results.data.movie_results[0],
            }
        });
    });
});

router.get('/person/:id', (req, res) => {
    const id = req.params.id;

    axios.get(TMDB_URL + 'find/' + id, {
        params: {
            api_key: TMDB_API_KEY,
            external_source: 'imdb_id'
        }
    }).then(results => {
        let personResults = results.data.person_results;
        if (personResults.length === 0) {
            res.send({message: 'ERR_NO_MOVIES'});
            return;
        }

        const personId = results.data.person_results[0].id;

        axios.get(TMDB_URL + 'person/' + personId, {
            params: {
                api_key: TMDB_API_KEY
            }
        }).then(result => {
            res.send({
                message: result.data
            });
        })
    });
});

router.get('/config', (_, res) => {
    axios.get(TMDB_URL + '/configuration', {
        params: {
            api_key: TMDB_API_KEY
        }
    }).then(result => res.send(result.data));
})

module.exports = router;