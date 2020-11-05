let questionId = $( ".poll-subject" )
    .data( "poll-id" )

let radio = $( ".radio-input" )

// get the number of vote to represent as percentage
$.ajax( {
    type: "get",
    url: `/api/poll/${questionId}/`,
    dataType: 'json',
    success: function ( data ) {
        useReturnData( data );
    }
} )

function useReturnData( data ) {
    let totalVote = 0;
    for ( i of data ) totalVote += i.vote
    data.push( totalVote )
    radio.click( data, voteResult )
}



function voteResult( e ) {
    $( radio )
        .unbind()
    let postData

    // increase total vote as the user voted
    e.data[ e.data.length - 1 ] += 1
    for ( let i of e.data ) {
        if ( i.option == this.innerText ) {
            postData = { 'id': i.id }
            i.vote += 1
        }

        i.percentage = Number( ( ( i.vote / e.data[ e.data.length - 1 ] ) * 100 )
            .toFixed( 2 ) )
    }

    // set option to the percentage
    for ( let j = 0; j < radio.length; j++ ) {
        $( radio[ j ] )
            .find( ".result" )
            .width( JSON.stringify( e.data[ j ].percentage ) + "%" )
    }

    // mark the voted option
    $( this )
        .removeClass( 'check' )
    $( this )
        .addClass( 'checked' )
        // sibling input
    let siblings = $( this )
        .siblings( ".radio-input" )
    siblings.removeClass( 'checked' )
    siblings.removeClass( 'check' )
    siblings.addClass( 'check' )

    // add percentage
    let percentages = $( radio )
        .find( ".percentage" )
    for ( let k = 0; k < percentages.length; k++ ) {
        $( percentages[ k ] )
            .html( e.data[ k ].percentage + "%" )
    }


    // mark browser voted
    let val = $( this )
        .find( "input" )
        .val()

    // send data back to server
    $.ajax( {
        type: "put",
        url: `/api/poll/${questionId}/`,
        dataType: 'json',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': Cookies.get( 'csrftoken' ),
            'Accept': 'application/json; indent=4',
        },
        data: JSON.stringify( postData ),
        success: function ( response ) {
            console.log( response );
        }
    } )
}
