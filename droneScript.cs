using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEditor;
using System.Linq;
using UnityEngine.Tilemaps;


public class droneScript : MonoBehaviour
{
    public Grid grid;
    
    public Vector2 pos;
    public Tilemap map;
    public float radius = 0.32f;
    public static List<scanPoint> scans = new List<scanPoint>();
    int path = 0;
    int timeFollowed = 11;
    int index;

    public class scanPoint : IComparable<scanPoint>, IEquatable<scanPoint>
    {
        public float x;
        public float y;
        private int value;

        public scanPoint(float x,float y, int value)
        {
            this.x = x;
            this.y = y;
            this.value = value;
        }

        public int getValue()
        {
            return value;
        }
        public int CompareTo(scanPoint other)
        {
            if (other.x > x) { return -1;}
            else if (other.x < x) { return 1;}
            else if(other.y > y) { return -1;}
            else if (other.y < y){ return 1; }
            
            return 0;
        }
        public bool Equals(scanPoint other)
        {
            if(other.x == x & other.y == y) { return true; }
            return false;
        }
        public bool isNear(scanPoint other, float range)
        {
            if((other.x < x + range & other.x > x-range) & (other.y < y + range & other.y > y - range))
            {
                return true;
            }
            return false;
        }
    }

    private void Start() {
           
        this.index = droneControl.drones.IndexOf(new Vector2(transform.position.x,transform.position.y));

    }
    public int[] isNearEdge()
    {
        
        var x = transform.position.x;
        var y = transform.position.y;
        if (x + 0.64f > 10.88)
        {
            return new int[] { 2,4,6 };
        }
        else if(x - 0.64 < -10.88)
        {
            return new int[] {3,5,7};
        }
        else if (y + 0.64 > 5.12)
        {
            return new int[] {0,4,5};
        }
        else if (y - 0.64 < -5.12)
        {
            return new int[] {1,6,7};
        }
        else { return new int[] {}; }
    }
    // Start is called before the first frame update

    // Update is called once per frame
    void Update()
    {
        
    }
    private void FixedUpdate()
    {
        // if (!avoid())
        // {            
        //     if (isNearEdge().Contains(path))
        //     {
        //         while (isNearEdge().Contains(path))
        //         {
        //             path = UnityEngine.Random.Range(0, 8);
        //             timeFollowed = 0;
        //         }
        //     }
        //     else if (timeFollowed > 50)
        //     {
        //         path = UnityEngine.Random.Range(0, 8);
        //         timeFollowed = 0;
        //     }
        //     float x = 0;
        //     float y = 0;

        //     if ((float)Math.Round(transform.position.x, 1) % 0.5 == 0) 
        //     {
        //         x = (float)Math.Round(transform.position.x, 1);
        //     }
        //     else
        //     {
        //         x = (float)Math.Round(transform.position.x, 0);
        //     }
        //     if ((float)Math.Round(transform.position.y, 1) % 0.5 == 0)
        //     {
        //         y = (float)Math.Round(transform.position.y, 1);
        //     }
        //     else
        //     {
        //         y = (float)Math.Round(transform.position.y, 0);
        //     }
        //     scanPoint sp = new scanPoint( x, y, getReading());
        //     if(!scans.Contains(sp))
        //     {
        //         scan(sp);
        //         move(path);

        //     }
        //     else
        //     {
        //         move(path);
        //     }
            
        //     timeFollowed++;

        // }
        transform.position = droneControl.drones[index];
        this.pos = transform.position;
        float x = 0;
        float y = 0;
        x = transform.position.x;
        y = transform.position.y;
        print(index+ ": " + transform.position + "  " + getReading());
            scanPoint sp = new scanPoint( x, y, getReading());
            if(!scans.Contains(sp))
            {
                scan(sp);
                move(path);

            }
    }   
    int getReading()
    {
        TileBase currTile = map.GetTile(grid.WorldToCell(transform.position));
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
        return -1;
    }

    void scan(scanPoint sp)
    {
        scans.Add(sp);
    }

    bool avoid()
    {
        //move(Random.Range(0, 4));
        Collider2D[] hits = Physics2D.OverlapCircleAll(
          transform.position,
          radius);
        //print(hits[0].name + " ===== " + gameObject.name + ": so " + hits[0].name.Equals(gameObject.name) + "???");

        if (hits.Length != 0)
        {
            float lowest = radius;
            GameObject lowestObj = gameObject;
            foreach (Collider2D collision in hits)
            {
                if (!collision.gameObject.name.Equals(gameObject.name))
                {
                    float dist = Vector3.Distance(transform.position, collision.transform.position);
                    if (dist < lowest)
                    {
                        lowest = dist;
                    }
                    lowestObj = collision.gameObject;
                }
            }
            if (!lowestObj.Equals(gameObject))
            {
                Vector3 dir = (transform.position - lowestObj.transform.position).normalized;
                //Debug.Log(gameObject.name + " moving " + dir);
                transform.position += dir * 0.1f;
                return true;
            }

        }
        return false;
    }
    private void OnCollisionStay2D(Collision2D collision)
    {


    }
   
    private void OnDrawGizmos()
    {
        //Gizmos.color = Color.green;
        //Gizmos.DrawWireSphere(transform.position, radius);
    }
    void move(int direction)
    {
        var speed = 0.032f;
        var speedD = 0.02262f;

        switch (direction)
        {
            case 0:
                transform.position = new Vector3(transform.position.x, transform.position.y + speed);
                break;
            case 1:
                transform.position = new Vector3(transform.position.x, transform.position.y - speed);
                break;
            case 2:
                transform.position = new Vector3(transform.position.x + speed, transform.position.y);
                break;
            case 3:
                transform.position = new Vector3(transform.position.x - speed, transform.position.y);
                break;
            case 4:
                transform.position = new Vector3(transform.position.x + speedD, transform.position.y + speedD);
                break;
            case 5:
                transform.position = new Vector3(transform.position.x - speedD, transform.position.y + speedD);
                break;
            case 6:
                transform.position = new Vector3(transform.position.x + speedD, transform.position.y - speedD);
                break;
            case 7:
                transform.position = new Vector3(transform.position.x - speedD, transform.position.y - speedD);
                break;
            default:
                break;
        }
    }

}


    


                

