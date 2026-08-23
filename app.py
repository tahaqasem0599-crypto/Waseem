using UnityEngine;

public class PubgShooting : MonoBehaviour {
    public GameObject bullet; // الرصاصة
    public Transform barrelEnd; // فوهة السلاح
    public float bulletSpeed = 2000f;

    void Update() {
        // عند الضغط على الماوس أو زر الإطلاق في الموبايل
        if (Input.GetButtonDown("Fire1")) {
            GameObject bulletInstance = Instantiate(bullet, barrelEnd.position, barrelEnd.rotation);
            bulletInstance.GetComponent<Rigidbody>().AddForce(barrelEnd.forward * bulletSpeed);
            Destroy(bulletInstance, 2f); // تدمير الرصاصة بعد ثانيتين لتوفير موارد الجهاز
        }
    }
}
