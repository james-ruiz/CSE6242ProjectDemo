import streamlit as st
import numpy as py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import statsmodels.formula.api as sm
import altair as alt
from load_data import data_prep
from footballfield import create_football_field
from load_data import team_colors
from load_data import all_data
from scipy import stats
import numpy as np
#from helpers import pearsonr_ci


def app():
  st.header("Win Probability and 4th Down Play Decision")
  df = data_prep() #fourthdown data
  #logos = team_logos()
  teamcolors = team_colors() #team colors
  all_df = all_data()
  


  


  def team_decisions(df):
    cola, colb = st.columns(2)
    with cola:
      teams = list(df["home_team"].unique())
      teams.sort()
      seasons = list(df['season'].unique())
      seasons.sort()
      team = st.selectbox(
      "Select a Team",
        (teams))
      season = st.selectbox( "Select a Season",
        (seasons)
      )
    
    
    with colb:

      if not team: st.error("Please select a team.")
      else:
        if not season:st.error("Please select a season")
        else:
          data = df[df["home_team"]==team]
          data = data[data["season"]==season]
          #keep_columns = ['game_id','game_date','play_type','ydstogo','away_team','game_seconds_remaining']
          #scoreboard_columns = ['qtr' , 'yardline_100' , 'play_type' , 'ydstogo' , 'game_seconds_remaining' , 'game_half' , 'side_of_field','posteam_score','defteam_score']
          #display_df = data[keep_columns]
          #display_df = display_df.rename(columns={"game_date": "Date", "play_type": "Play Type", "ydstogo": "Yards to Go"}, errors="raise")
        

        #get key by combining columns
        
          data['game_list'] ='Game On ' + data['game_date'].astype(str) +" vs "+ data['away_team']
          game_list = list(data['game_list'].unique())
          game = st.selectbox("Choose a Game",(game_list))
          #st.write("Team "+team+" decisions", display_df.sort_index())
         
          data = data[data["game_list"]==game]
          game_id = list(data['game_id'].unique())
          against_team = list(data['away_team'].unique()) 
          data = data[data['posteam']==team]


#keep_columns = ['season','home_team','away_team','down','game_date','game_half','game_seconds_remaining', 'play_type', 'ydstogo','yardline_100', 'posteam', 'qtr','side_of_field', 'defteam', 'side_of_field','posteam_score','defteam_score','roof','surface','temp','wind','stadium']
        
         # col1,col2 = st.columns(2)

          #with col1:
            #st.image('images/'+team+'.png')
         
          data['Decision'] = 'Quarter: ' + data['qtr'].astype(str) + ', Time Remining [seconds]:  ' + data['game_seconds_remaining'].astype(int).astype(str) + ', Yards to Go: '+ data['ydstogo'].astype(str)
          decisions = list(data['Decision'].unique()) 

         # with col2:

          #  st.image('images/'+' '.join(against_team) +'.png') 
          #st.markdown("Show the Scoreboard")
          decision = st.selectbox( "Choose 4th Down Scenario",(decisions))
         
    plot_df = data[data['Decision']==decision]
    decision_time = list((60.0-(plot_df['game_seconds_remaining']/60)).astype(int))
    decision_play = list(plot_df['play_id'])
    #plot_df = plot_df[scoreboard_columns]

    colA,colB,colC = st.columns(3)

    with colA:
      logA, logB = st.columns(2)
      with logA:
        st.image('images/'+team+'.png')
        #st.markdown("Team in posesion of ball")
      with logB:
        pt_score = plot_df['posteam_score'].astype(int).astype(str)
        st.subheader('Score')
        score_pos = '<p style="font-family:sans-serif; color:Blue; font-size: 58px;">'+ ''.join(pt_score)+' </p>'
        st.markdown(score_pos, unsafe_allow_html=True)
       
    with colB:
      st.subheader("Game Status")
      score1,score2,score3 = st.columns(3)
      with score1:
        st.markdown('Quarter')
        quarter = plot_df['qtr'].astype(str)
        quarter_info =  '<p style="font-family:sans-serif; color:blue; font-size: 30px; alignment:center;">'+ ''.join(quarter)+' </p>'
        st.markdown(quarter_info, unsafe_allow_html=True)
      with score2:
        st.markdown('Yardine')
        # yard_line = np.where(plot_df['yardline_100']>50, 100-plot_df['yardline_100'], plot_df['yardline_100']).astype(int).astype(str)
        yard_line = plot_df['yardline_100'].astype(int).astype(str)
        yard_info =  '<p style="font-family:sans-serif; color:blue; font-size: 30px;alignment:center;">'+ ''.join(yard_line)+' </p>'
        st.markdown(yard_info, unsafe_allow_html=True)
      with score3:
        st.markdown('Yards to Go')
        ydstogo = plot_df['ydstogo'].astype(str)
        quarter_info =  '<p style="font-family:sans-serif; color:blue; font-size: 30px;alignment:center;">'+ ''.join(ydstogo)+' </p>'
        st.markdown(quarter_info, unsafe_allow_html=True)
      








    with colC:
      away1, away2 = st.columns(2)
      with away1:
        st.image('images/'+' '.join(against_team) +'.png')
      with away2:
        dt_score = plot_df['defteam_score'].astype(int).astype(str)
        st.subheader('Score')
        score_def = '<p style="font-family:sans-serif; color:Blue; font-size: 58px;">'+ ''.join(dt_score)+' </p>'
        st.markdown(score_def, unsafe_allow_html=True)
        

    
    #color_pos = teamcolors[teamcolors['team']==team]
    #colorA = color_pos['color'].astype(str)      

    #plt.figure()
    #sns.lineplot(data=game_df, palette="tab10", linewidth=2.5)
    #sns.catplot(data=data,x='play_type', y='ydstogo',kind='box', palette='plasma')
    #plt.xticks(rotation=45)
    #st.pyplot(plt)
    #plt.figure()


       

    game_df = all_df[all_df['game_id']==game_id[0]]
    team1 = list(plot_df['home_team'].unique())
    team2 = list(plot_df['away_team'].unique())
    game_teams = [team1[0],team2[0]]

    cols_graphic = ['home_team_pred_proba_plus','away_team_pred_proba_plus','game_seconds_remaining']


     
    colors = []
    for t in game_teams:
      colors.append(teamcolors[teamcolors["team"]==t]['color'].tolist()[0])
    

    graph_data = game_df[cols_graphic]
    graph_data['minutes_remaining'] = (graph_data['game_seconds_remaining']/60).astype(int)
    graph_data = graph_data.drop(columns=['game_seconds_remaining'])
    
    graph_data = graph_data[graph_data['minutes_remaining']>=decision_time[0]]
    graph_data = graph_data.set_index("minutes_remaining").sort_index(ascending=False).rename(columns={"home_team_pred_proba_plus":game_teams[0],
                                "away_team_pred_proba_plus":game_teams[1]})


    tab1, tab2, tab3 = st.columns(3)#["Field Position", "Win Probability chart", 'Decision Options'])
    
    

    with tab1:
      st.write("     Field Position: "+team1[0])
      plt.figure()

      yl=100-yard_line.astype(int)
      yt=ydstogo.astype(int)
      fig, ax = create_football_field(highlight_line=True,
                                highlight_line_number=yl, yards_to_go=yt)

      plt.xlim(0, 120)
      plt.ylim(0, 53.5)
      plt.vlines(x=yl+10+yt,
           ymin=-5,
           ymax=58.3,
           colors=["yellow","yellow"],
           linestyles="dashed",
           linewidth=2)#"dashed"

      plt.text(5, 25, game_teams[0],
         size="x-large", 
         rotation=90,
         color="white")

      plt.text(112, 25, game_teams[1],
         size="x-large", 
         rotation=270,
         color="white")
    
      st.pyplot(plt)
      plt.figure() 

  

    with tab2:

      # plt.figure(figsize=(6.4,4)) #width, height 6.4, 4.8
      plt.figure()
      sns.lineplot(data=graph_data, palette=colors, linewidth=1.5, errorbar=None)
      #sns.catplot(data=data,x='play_type', y='ydstogo',kind='box', palette='plasma')
      #ax.axvline(decision_time, color="darkred", linestyle="-", label="Valentine's Day")
      plt.xticks(rotation=0)
      plt.xlim(60,0)
      plt.ylim(0,1)
      plt.xlabel("Time Remaining [minutes]")
      plt.ylabel("Win Probability")
      #plt.title(f"Win Probability Chart\n{game_teams[0]} vs {game_teams[1]}")
      plt.title(f"Win Probability: {game_teams[0]} vs {game_teams[1]}")
      st.pyplot(plt)
      plt.figure()

    with tab3:
        
      play_columns               = ['play_id','posteam_fg_made_wp_delta', 'posteam_fg_missed_wp_delta', 'posteam_punt_wp_delta','posteam_pass_failed_wp_delta', 'posteam_run_failed_wp_delta', 'posteam_pass_convert_wp_delta', 'posteam_run_convert_wp_delta']
      column_graph               = plot_df[plot_df['play_id']==decision_play[0]]
      column_graph               = column_graph[play_columns]
      column_graph['Punt']       = column_graph['posteam_punt_wp_delta']
      column_graph['Field Goal'] = column_graph['posteam_fg_made_wp_delta']+column_graph['posteam_fg_missed_wp_delta']
      column_graph['Run']        = column_graph['posteam_run_failed_wp_delta'] + column_graph['posteam_run_convert_wp_delta']
      column_graph['Pass']       = column_graph['posteam_pass_failed_wp_delta'] + column_graph['posteam_pass_convert_wp_delta']
      column_graph               = column_graph.drop(columns=['posteam_fg_made_wp_delta', 'posteam_fg_missed_wp_delta', 'posteam_punt_wp_delta','posteam_pass_failed_wp_delta', 'posteam_run_failed_wp_delta', 'posteam_pass_convert_wp_delta', 'posteam_run_convert_wp_delta'])
      graph_df                   = column_graph.melt(id_vars='play_id', var_name='Play',value_vars=['Punt','Field Goal','Run','Pass'], value_name='Probability')

      # c = [colors[0] if (x < max(graph_df.Probability)) else '#66ff66' for x in graph_df.Probability]
      
      c = ['#bababa' if (x < max(graph_df.Probability)) else '#66ff66' for x in graph_df.Probability]
      
      #bababa
      
      # plt.figure(figsize=(6.4,4)) #width, height 6.4, 4.8
      plt.figure()
      ax=sns.barplot(data=graph_df, x=graph_df.Play, y=graph_df.Probability, palette=c)
      plt.xlabel("Play Type")
      plt.ylabel("Change in Win Probability")
      plt.title(f"Change in Win Probability by Play Type: {game_teams[0]}")
      #plt.title(f"Change in Win Probability by Play Type for team \n{game_teams[0]}")
      st.pyplot(plt)
      plt.figure()
    
  
  team_decisions(df)
  #plt.show()

  

  
