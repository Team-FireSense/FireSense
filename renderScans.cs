using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.Tilemaps;

public class renderScans : MonoBehaviour
{
    public Grid grid;

    public Tilemap map;
    public Sprite cir;
    int update = 0;
    int size = 0;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void fixedUpdate()
    {
        if(update == 5)
        {
            draw();
            update = 0;
        }
        else
        {
            update++;
        }

    }
    
    void draw()
    {

        for (int i = 0 + size; i < droneScript.scans.Count; i++)
        {
            var sp = droneScript.scans[i];
            var circle = new GameObject();
            circle.AddComponent<SpriteRenderer>();
            circle.GetComponent<SpriteRenderer>().sprite = cir;
            if (sp.getValue() == 1)
            {
                circle.GetComponent<SpriteRenderer>().color = new Color(150f / 255f, 150f / 255f, 150f / 255f);
            }
            else if (sp.getValue() == 2)
            {
                circle.GetComponent<SpriteRenderer>().color = new Color(231f / 255f, 148f / 255f, 115f / 255f);
            }
            else if (sp.getValue() == 3)
            {
                circle.GetComponent<SpriteRenderer>().color = new Color(225f / 255f, 96f / 255f, 44f / 255f);
            }
            else if (sp.getValue() == 4)
            {
                circle.GetComponent<SpriteRenderer>().color = new Color(222f / 255f, 63f / 255f, 0 / 255f);
            }
            circle.transform.localScale = new Vector3(0.32f, 0.32f, 1);
            circle.transform.position = new Vector3(sp.x + 28.3f, sp.y);
            circle.transform.parent = transform;

            circle.name = "dataPoint";

        }
        size = droneScript.scans.Count;
    }


}


//switch (direction)
//{
//    case 0:
//        transform.position = new Vector3(transform.position.x, transform.position.y + speed);
//        break;
//    case 1:
//        transform.position = new Vector3(transform.position.x, transform.position.y - speed);
//        break;
//    case 2:
//        transform.position = new Vector3(transform.position.x + speed, transform.position.y);
//        break;
//    case 3:
//        transform.position = new Vector3(transform.position.x - speed, transform.position.y);
//        break;
//    case 4:
//        transform.position = new Vector3(transform.position.x + speedD, transform.position.y + speedD);
//        break;
//    case 5:
//        transform.position = new Vector3(transform.position.x - speedD, transform.position.y + speedD);
//        break;
//    case 6:
//        transform.position = new Vector3(transform.position.x + speedD, transform.position.y - speedD);
//        break;
//    case 7:
//        transform.position = new Vector3(transform.position.x - speedD, transform.position.y - speedD);
//        break;
//    default:
//        break;
//}