$(function(){

    axios.get('/movies').then(function(response){
        for (let movie of response.data) {
            let html= `<ul>
                <li>Title:${movie.title}</li>
                <li>Plot:${movie.plot}</li>
            </ul>
            `;

            $('#movies').append( $(html))

        }
    })

    $('#add-movie-btn').click(function(){
        let movie_title = $('#title-input').val()
        let plot = $('#plot-input').val()
        axios.post('/movie/create', {
            title:movie_title,
            plot:plot
        }).then(function(response){
            console.log(response.data)
        })
    })
})