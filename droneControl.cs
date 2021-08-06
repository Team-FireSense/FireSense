using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.Tilemaps;


public class droneControl : MonoBehaviour
{
    //controls each indivudal drone with positions as childs of Transform.
    public Grid grid;
    
    public Tilemap map;
    public static List<Vector2> drones = new List<Vector2>();

    PSO pso;

    Boolean stopped = false;
    // Start is called before the first frame update
    void Awake()
    {
        var velocities = new List<Vector2>();

        foreach (Transform child in transform)
            {
               var pos = new Vector2(child.position.x,child.position.y);
               drones.Add(pos);
               print(pos);
               //Randomizes velocity to begin PSO
               velocities.Add(new Vector2(UnityEngine.Random.Range(-0.02f,0.02f),UnityEngine.Random.Range(-0.02f,0.02f)));
            }
        pso = new PSO(drones,velocities,fitness_function);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        if(!stopped){
            print("damjd");
            stopped = pso.next();
        }
        var list = new List<Vector2>();
        foreach(Vector2 pos in pso.particles){
            list.Add(pos);
        }
        //stores positions of drones as a list
        drones = list;

    }
    List<float> fitness_function(List<Vector2> positions){
        var values = new List<float>();
        foreach(Vector2 vec in positions){
            values.Add(getReading(vec));
            //    print("pos==== "+vec);

        }
        
        return values;
    }

    int getReading(Vector2 vec)
    {
        TileBase currTile = map.GetTile(grid.WorldToCell(vec));
        if (currTile != null)
        {
            if (currTile.name.Equals("blankTile"))
            {
                return 4;
            }
            if (currTile.name.Equals("lowHeatTile"))
            {
                return 3;
            }
            if (currTile.name.Equals("medHeatTile"))
            {
                return 2;
            }
            if (currTile.name.Equals("highHeatTile"))
            {
                return 1;
            }
        }
        return 5;
    }
}
public class PSO{
    
    public List<Vector2> particles;
    public List<Vector2> velocities;
    public float w;
    public float c_1;
    public float c_2;
    float max_iter;

    bool auto_coef; 
    List<Vector2> pbests;  
    public List<Vector2> gbest; 
    int iter;
    int N;
    Boolean is_running;
    
    Func<List<Vector2>,List<float>> fitness_function;
    List<float> p_bests_values;

    Vector2 gbestShort;
    float g_best_value;
    public PSO(List<Vector2> particles, List<Vector2> velocities, Func<List<Vector2>,List<float>> fitness_function,
                 float w = 0.8f, float c_1=1, float c_2=1, float max_iter=100, bool auto_coef=true)
                 {
                     this.particles = particles;
                     this.velocities = velocities;
                     this.N = particles.Count;
                     this.w = w;
                     this.c_1 = c_1;
                     this.c_2 = c_2;
                     this.auto_coef = auto_coef;
                     this.max_iter = max_iter;
                     this.fitness_function = fitness_function;
                     this.pbests = this.particles;
                     this.p_bests_values = this.fitness_function(this.particles);
                     this.gbest = this.pbests;
                     this.gbestShort = this.pbests[0];
                     this.g_best_value = this.p_bests_values[0];
                     this.updateBests();
                     this.iter = 0;
                     this.is_running = true;
                     this.updateCoef();
                    
                     
                     }

    void printPB(){
        for(int i = 0; i<p_bests_values.Count;i++){
          Debug.Log("PB: "+i+"=========="+p_bests_values[i]);
        }
    }
                
    public Boolean next(){
        
        if(iter < max_iter){
            Debug.Log("iter: "+ iter);
            moveParticles();
            updateBests();
            updateCoef();
        }
        this.iter +=1;
        this.is_running = this.is_running &&  this.iter<this.max_iter;
        return this.is_running;
    }

    void moveParticles(){
        
        var newVelocities = new List<Vector2>();
        foreach(Vector2 v in velocities){
            newVelocities.Add(v*w);
            
        }
    
        
        var r_1 = new List<Vector2>();
        for(var i = 0;i<N;i++){
            var rand = UnityEngine.Random.Range(0f,1f);
            r_1.Add(new Vector2(rand,rand));
        }
        for(var i = 0; i<newVelocities.Count; i++){
           //PSO algorithm with hyperparemters c_1, r_1.

            var vel = new Vector2(c_1*r_1[i].x*(pbests[i].x-particles[i].x), this.c_1*r_1[i].y*(this.pbests[i].y-this.particles[i].y));

            newVelocities[i] += vel;
            // Debug.Log("First Vel "+newVelocities[i]);

        }

        var r_2 = new List<Vector2>();
        for(var i = 0;i<N;i++){
            var rand = UnityEngine.Random.Range(0f,1f);
            r_2.Add(new Vector2(rand,rand));

        }
        for(var i = 0; i<newVelocities.Count; i++){
  
            newVelocities[i] += new Vector2(this.c_2*r_2[i].x*(this.gbest[i].x-this.particles[i].x), this.c_2*r_2[i].y*(this.gbest[i].y-this.particles[i].y));
       
        }

        
        var list = new List<Vector2>();
        for(var i = 0;i<N;i++){
            list.Add(gbestShort);
        }
        gbest = list;

        var total = 0f;
        for(int i = 0;i<velocities.Count;i++){
            var vec = (velocities[i]-newVelocities[i]);
            total += vec.x + vec.y;

        }
        
        if(total != 0){
            is_running = false;
        }
        foreach(Vector2 v in newVelocities){
            //    Debug.Log("vel==== "+v);
        }
        velocities = newVelocities;
        for(int i=0; i<particles.Count; i++){
            particles[i]+= newVelocities[i];
            // Debug.Log("final vel--------------"+particles[i]);
        }
        
    }
    void addVels(){
        for(int i = 0; i<particles.Count;i++) {
            particles[i] += velocities[i];
        }
    }
    void updateCoef(){
        if (this.auto_coef){
            int t = this.iter;
            float n = this.max_iter;
            this.w = 0.4f/(float)Math.Pow(n,2)* (float)Math.Pow(t-n,2)+ 0.4f;
            this.c_1 = -3*t/n + (float)3.5;
            this.c_2 = 3*t/n + (float)0.5;

        }
    }
    void updateBests(){
        var fits = fitness_function(this.particles) ;
        
        for (int i = 0; i<this.particles.Count; i++){
            //Update drone behavior uing fitness function using loop.
            Debug.Log("fit: "+i+" i======"+fits[i]);
             if (fits[i] <= this.p_bests_values[i]){
                Debug.Log(fits[i]);
                this.p_bests_values[i] = fits[i];
                this.pbests[i] = this.particles[i];
                Debug.Log("fitness: " + fits[i]);

                if (fits[i] <= this.g_best_value){
                    this.g_best_value = fits[i];
                    //Debug.Log(g_best_value);
                    this.gbestShort = this.particles[i];
                    //Debug.Log(gbestShort);
             }
             }

        }
        Debug.Log("gbests"+ gbest[0] + "  gbest_value"+g_best_value);
    }
}
